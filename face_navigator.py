#!/usr/bin/env python3
"""
Face Navigation App for Ubuntu
Uses face tracking for cursor movement and eye blinks for mouse clicks
"""

import cv2
import dlib
import numpy as np
import pyautogui
import time
import json
import os
import argparse
from scipy.spatial import distance as dist
from imutils import face_utils
import threading
import logging

class FaceNavigator:
    def __init__(self, config_file="config.json"):
        self.config_file = config_file
        self.load_config()
        
        # Initialize face detection and landmark prediction
        self.face_detector = dlib.get_frontal_face_detector()
        
        # Download shape predictor if not exists
        self.shape_predictor_path = "shape_predictor_68_face_landmarks.dat"
        if not os.path.exists(self.shape_predictor_path):
            print("Downloading facial landmark predictor...")
            self.download_shape_predictor()
        
        self.landmark_predictor = dlib.shape_predictor(self.shape_predictor_path)
        
        # Eye landmark indices
        self.LEFT_EYE_POINTS = list(range(42, 48))
        self.RIGHT_EYE_POINTS = list(range(36, 42))
        
        # Initialize camera
        self.camera = cv2.VideoCapture(0)
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        # Screen dimensions
        self.screen_width, self.screen_height = pyautogui.size()
        
        # Face tracking variables
        self.face_center_baseline = None
        self.calibrated = False
        self.calibration_frames = 0
        self.calibration_required = 30  # frames
        
        # Blink detection variables
        self.eye_ar_threshold = self.config['eye_ar_threshold']
        self.eye_ar_consecutive_frames = self.config['eye_ar_consecutive_frames']
        self.left_eye_counter = 0
        self.right_eye_counter = 0
        self.last_blink_time = time.time()
        self.blink_cooldown = self.config['blink_cooldown']
        
        # Movement smoothing
        self.smoothing_factor = self.config['smoothing_factor']
        self.last_cursor_pos = pyautogui.position()
        
        # Setup logging
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)
        
        # Disable pyautogui failsafe (optional)
        pyautogui.FAILSAFE = False
    
    def load_config(self):
        """Load configuration from JSON file"""
        default_config = {
            "sensitivity": 2.0,
            "eye_ar_threshold": 0.25,
            "eye_ar_consecutive_frames": 3,
            "blink_cooldown": 0.5,
            "smoothing_factor": 0.7,
            "movement_threshold": 10,
            "calibration_region_size": 50
        }
        
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                self.config = json.load(f)
                # Add any missing keys from default config
                for key, value in default_config.items():
                    if key not in self.config:
                        self.config[key] = value
        else:
            self.config = default_config
            self.save_config()
    
    def save_config(self):
        """Save configuration to JSON file"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=4)
    
    def download_shape_predictor(self):
        """Download the dlib facial landmark predictor"""
        import urllib.request
        import bz2
        
        url = "http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2"
        compressed_file = "shape_predictor_68_face_landmarks.dat.bz2"
        
        try:
            print("Downloading facial landmark predictor...")
            urllib.request.urlretrieve(url, compressed_file)
            
            print("Extracting...")
            with bz2.BZ2File(compressed_file, 'rb') as f_in:
                with open(self.shape_predictor_path, 'wb') as f_out:
                    f_out.write(f_in.read())
            
            os.remove(compressed_file)
            print("Download complete!")
            
        except Exception as e:
            print(f"Error downloading shape predictor: {e}")
            print("Please download shape_predictor_68_face_landmarks.dat manually")
            raise
    
    def calculate_eye_aspect_ratio(self, eye_landmarks):
        """Calculate eye aspect ratio for blink detection"""
        # Vertical eye landmarks
        A = dist.euclidean(eye_landmarks[1], eye_landmarks[5])
        B = dist.euclidean(eye_landmarks[2], eye_landmarks[4])
        
        # Horizontal eye landmark
        C = dist.euclidean(eye_landmarks[0], eye_landmarks[3])
        
        # Eye aspect ratio
        ear = (A + B) / (2.0 * C)
        return ear
    
    def calibrate_face_center(self, face_center):
        """Calibrate baseline face position"""
        if not self.calibrated:
            if self.face_center_baseline is None:
                self.face_center_baseline = np.array(face_center, dtype=np.float32)
                self.calibration_frames = 1
            else:
                # Running average
                alpha = 0.1
                self.face_center_baseline = (1 - alpha) * self.face_center_baseline + alpha * np.array(face_center)
                self.calibration_frames += 1
            
            if self.calibration_frames >= self.calibration_required:
                self.calibrated = True
                self.logger.info("Face calibration complete!")
    
    def move_cursor_with_face(self, face_center):
        """Move cursor based on face movement"""
        if not self.calibrated:
            return
        
        # Calculate face movement relative to baseline
        movement = np.array(face_center) - self.face_center_baseline
        
        # Apply sensitivity and scaling
        cursor_movement = movement * self.config['sensitivity']
        
        # Apply movement threshold to reduce jitter
        if np.linalg.norm(cursor_movement) < self.config['movement_threshold']:
            return
        
        # Get current cursor position
        current_x, current_y = pyautogui.position()
        
        # Calculate new position
        new_x = current_x + cursor_movement[0]
        new_y = current_y - cursor_movement[1]  # Invert Y axis
        
        # Apply smoothing
        smooth_x = self.smoothing_factor * self.last_cursor_pos[0] + (1 - self.smoothing_factor) * new_x
        smooth_y = self.smoothing_factor * self.last_cursor_pos[1] + (1 - self.smoothing_factor) * new_y
        
        # Clamp to screen boundaries
        smooth_x = max(0, min(self.screen_width - 1, smooth_x))
        smooth_y = max(0, min(self.screen_height - 1, smooth_y))
        
        # Move cursor
        pyautogui.moveTo(smooth_x, smooth_y)
        self.last_cursor_pos = (smooth_x, smooth_y)
    
    def detect_blinks(self, landmarks):
        """Detect eye blinks and perform clicks"""
        current_time = time.time()
        
        # Skip if still in cooldown period
        if current_time - self.last_blink_time < self.blink_cooldown:
            return
        
        # Extract eye landmarks
        left_eye = landmarks[self.LEFT_EYE_POINTS]
        right_eye = landmarks[self.RIGHT_EYE_POINTS]
        
        # Calculate eye aspect ratios
        left_ear = self.calculate_eye_aspect_ratio(left_eye)
        right_ear = self.calculate_eye_aspect_ratio(right_eye)
        
        # Check for left eye blink
        if left_ear < self.eye_ar_threshold:
            self.left_eye_counter += 1
        else:
            if self.left_eye_counter >= self.eye_ar_consecutive_frames:
                self.logger.info("Left eye blink detected - Left click")
                pyautogui.click(button='left')
                self.last_blink_time = current_time
            self.left_eye_counter = 0
        
        # Check for right eye blink
        if right_ear < self.eye_ar_threshold:
            self.right_eye_counter += 1
        else:
            if self.right_eye_counter >= self.eye_ar_consecutive_frames:
                self.logger.info("Right eye blink detected - Right click")
                pyautogui.click(button='right')
                self.last_blink_time = current_time
            self.right_eye_counter = 0
    
    def run(self, show_video=False):
        """Main application loop"""
        self.logger.info("Starting Face Navigator...")
        self.logger.info("Look straight ahead and keep your face steady for calibration...")
        
        try:
            while True:
                ret, frame = self.camera.read()
                if not ret:
                    self.logger.error("Failed to capture frame")
                    break
                
                # Flip frame horizontally for mirror effect
                frame = cv2.flip(frame, 1)
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                
                # Detect faces
                faces = self.face_detector(gray)
                
                if len(faces) > 0:
                    # Use the first detected face
                    face = faces[0]
                    
                    # Get facial landmarks
                    landmarks = self.landmark_predictor(gray, face)
                    landmarks = face_utils.shape_to_np(landmarks)
                    
                    # Calculate face center
                    face_center = np.mean(landmarks, axis=0)
                    
                    # Calibrate or move cursor
                    if not self.calibrated:
                        self.calibrate_face_center(face_center)
                        if show_video:
                            cv2.putText(frame, f"Calibrating... {self.calibration_frames}/{self.calibration_required}", 
                                      (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                    else:
                        self.move_cursor_with_face(face_center)
                        self.detect_blinks(landmarks)
                    
                    if show_video:
                        # Draw face landmarks
                        for (x, y) in landmarks:
                            cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)
                        
                        # Draw face rectangle
                        cv2.rectangle(frame, (face.left(), face.top()), 
                                    (face.right(), face.bottom()), (255, 0, 0), 2)
                        
                        # Draw face center
                        cv2.circle(frame, tuple(face_center.astype(int)), 5, (0, 0, 255), -1)
                
                if show_video:
                    cv2.imshow('Face Navigator', frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                
                # Small delay to prevent excessive CPU usage
                time.sleep(0.01)
                
        except KeyboardInterrupt:
            self.logger.info("Stopping Face Navigator...")
        except Exception as e:
            self.logger.error(f"Error in main loop: {e}")
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Clean up resources"""
        self.camera.release()
        cv2.destroyAllWindows()
        self.logger.info("Face Navigator stopped")

def main():
    parser = argparse.ArgumentParser(description='Face Navigation App for Ubuntu')
    parser.add_argument('--show-video', action='store_true', 
                       help='Show video feed window (useful for debugging)')
    parser.add_argument('--config', default='config.json',
                       help='Configuration file path')
    
    args = parser.parse_args()
    
    try:
        navigator = FaceNavigator(config_file=args.config)
        navigator.run(show_video=args.show_video)
    except Exception as e:
        print(f"Error starting Face Navigator: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())