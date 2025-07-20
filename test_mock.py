#!/usr/bin/env python3
"""
Simplified test version of Face Navigator for validation
"""

import sys
import json
import os
import argparse
import time

class MockFaceNavigator:
    """Mock version for testing without dependencies"""
    
    def __init__(self, config_file="config.json"):
        self.config_file = config_file
        self.load_config()
        print(f"✓ Config loaded from {config_file}")
        
        # Mock initialization
        self.calibrated = False
        self.calibration_frames = 0
        print("✓ Mock Face Navigator initialized")
    
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
    
    def run(self, show_video=False):
        """Mock run method"""
        print("✓ Mock Face Navigator started")
        print(f"  Show video: {show_video}")
        print(f"  Sensitivity: {self.config['sensitivity']}")
        print(f"  Eye threshold: {self.config['eye_ar_threshold']}")
        
        # Simulate calibration
        print("✓ Mock calibration phase...")
        for i in range(3):
            time.sleep(0.1)
            print(f"  Calibrating... {i+1}/3")
        
        print("✓ Mock calibration complete")
        print("✓ Mock face tracking would start here")
        print("✓ Mock blink detection would be active")
        
        return True

def main():
    parser = argparse.ArgumentParser(description='Face Navigation App for Ubuntu (Test Mode)')
    parser.add_argument('--show-video', action='store_true', 
                       help='Show video feed window (mock)')
    parser.add_argument('--config', default='config.json',
                       help='Configuration file path')
    
    args = parser.parse_args()
    
    print("Face Navigator - Test Mode")
    print("=" * 40)
    
    try:
        navigator = MockFaceNavigator(config_file=args.config)
        navigator.run(show_video=args.show_video)
        print("✓ Test completed successfully")
        return 0
    except Exception as e:
        print(f"✗ Test failed: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())