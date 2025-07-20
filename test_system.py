#!/usr/bin/env python3
"""
Test script for Face Navigator
Tests basic functionality without requiring full setup
"""

import sys
import importlib

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")
    
    required_modules = [
        'cv2',
        'numpy', 
        'scipy',
        'pyautogui',
        'imutils'
    ]
    
    missing_modules = []
    
    for module in required_modules:
        try:
            importlib.import_module(module)
            print(f"✓ {module}")
        except ImportError:
            print(f"✗ {module} - MISSING")
            missing_modules.append(module)
    
    if missing_modules:
        print(f"\nMissing modules: {', '.join(missing_modules)}")
        print("Please run: pip install -r requirements.txt")
        return False
    else:
        print("\nAll modules imported successfully!")
        return True

def test_camera():
    """Test camera access"""
    print("\nTesting camera access...")
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("✗ Camera not accessible")
            return False
        
        ret, frame = cap.read()
        if not ret:
            print("✗ Cannot read from camera")
            cap.release()
            return False
        
        print(f"✓ Camera working - Frame size: {frame.shape}")
        cap.release()
        return True
        
    except Exception as e:
        print(f"✗ Camera test failed: {e}")
        return False

def test_screen_info():
    """Test screen information"""
    print("\nTesting screen information...")
    try:
        import pyautogui
        screen_size = pyautogui.size()
        print(f"✓ Screen size: {screen_size}")
        
        current_pos = pyautogui.position()
        print(f"✓ Current cursor position: {current_pos}")
        return True
        
    except Exception as e:
        print(f"✗ Screen test failed: {e}")
        return False

def test_face_detection():
    """Test basic face detection"""
    print("\nTesting face detection...")
    try:
        import cv2
        import dlib
        
        # Test if we can initialize face detector
        detector = dlib.get_frontal_face_detector()
        print("✓ Face detector initialized")
        
        # Note: We skip landmark predictor test since it requires download
        print("Note: Facial landmark predictor will be downloaded on first run")
        return True
        
    except Exception as e:
        print(f"✗ Face detection test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("Face Navigator - System Test")
    print("=" * 40)
    
    tests = [
        test_imports,
        test_camera,
        test_screen_info,
        test_face_detection
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 40)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("\n✓ All tests passed! Face Navigator should work correctly.")
        print("Run: python3 face_navigator.py --show-video")
        return 0
    else:
        print(f"\n✗ {total - passed} test(s) failed. Please resolve issues before running Face Navigator.")
        return 1

if __name__ == "__main__":
    sys.exit(main())