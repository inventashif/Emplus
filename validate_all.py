#!/usr/bin/env python3
"""
Comprehensive validation test for Face Navigator
Tests file structure, permissions, and integration
"""

import os
import stat
import json
import sys

def test_file_structure():
    """Test that all required files exist"""
    print("Testing file structure...")
    
    required_files = [
        'face_navigator.py',
        'requirements.txt',
        'install.sh',
        'run.sh',
        'config.json',
        'README.md',
        'README_FaceNavigator.md',
        'test_system.py',
        'test_mock.py',
        '.gitignore',
        'face-navigator.desktop'
    ]
    
    missing_files = []
    
    for filename in required_files:
        if os.path.exists(filename):
            print(f"✓ {filename}")
        else:
            print(f"✗ {filename} - MISSING")
            missing_files.append(filename)
    
    if missing_files:
        print(f"\nMissing files: {', '.join(missing_files)}")
        return False
    else:
        print("\n✓ All required files present")
        return True

def test_executable_permissions():
    """Test that scripts have executable permissions"""
    print("\nTesting executable permissions...")
    
    executable_files = [
        'install.sh',
        'run.sh',
        'test_system.py',
        'test_mock.py'
    ]
    
    permission_errors = []
    
    for filename in executable_files:
        if os.path.exists(filename):
            file_stat = os.stat(filename)
            is_executable = bool(file_stat.st_mode & stat.S_IEXEC)
            if is_executable:
                print(f"✓ {filename} - executable")
            else:
                print(f"✗ {filename} - not executable")
                permission_errors.append(filename)
    
    if permission_errors:
        print(f"\nFiles need executable permission: {', '.join(permission_errors)}")
        print("Run: chmod +x " + " ".join(permission_errors))
        return False
    else:
        print("\n✓ All scripts are executable")
        return True

def test_configuration():
    """Test configuration file structure"""
    print("\nTesting configuration...")
    
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
        
        required_config_keys = [
            'sensitivity',
            'eye_ar_threshold', 
            'eye_ar_consecutive_frames',
            'blink_cooldown',
            'smoothing_factor',
            'movement_threshold',
            'calibration_region_size'
        ]
        
        missing_keys = [key for key in required_config_keys if key not in config]
        
        if missing_keys:
            print(f"✗ Missing config keys: {missing_keys}")
            return False
        
        # Validate value ranges
        validations = [
            ('sensitivity', config['sensitivity'] > 0),
            ('eye_ar_threshold', 0.1 <= config['eye_ar_threshold'] <= 0.5),
            ('eye_ar_consecutive_frames', 1 <= config['eye_ar_consecutive_frames'] <= 10),
            ('blink_cooldown', 0.1 <= config['blink_cooldown'] <= 2.0),
            ('smoothing_factor', 0.0 <= config['smoothing_factor'] <= 1.0),
            ('movement_threshold', config['movement_threshold'] >= 0),
            ('calibration_region_size', config['calibration_region_size'] > 0)
        ]
        
        invalid_values = []
        for key, is_valid in validations:
            if is_valid:
                print(f"✓ {key}: {config[key]}")
            else:
                print(f"✗ {key}: {config[key]} - invalid range")
                invalid_values.append(key)
        
        if invalid_values:
            print(f"\nInvalid config values: {', '.join(invalid_values)}")
            return False
        
        print("\n✓ Configuration is valid")
        return True
        
    except json.JSONDecodeError as e:
        print(f"✗ config.json - Invalid JSON: {e}")
        return False
    except Exception as e:
        print(f"✗ Configuration test failed: {e}")
        return False

def test_main_script():
    """Test main script structure"""
    print("\nTesting main script...")
    
    try:
        with open('face_navigator.py', 'r') as f:
            content = f.read()
        
        required_imports = [
            'import cv2',
            'import dlib', 
            'import numpy',
            'import pyautogui',
            'from scipy.spatial import distance',
            'from imutils import face_utils'
        ]
        
        missing_imports = []
        for imp in required_imports:
            if imp in content:
                print(f"✓ {imp}")
            else:
                print(f"✗ {imp} - not found")
                missing_imports.append(imp)
        
        # Check for main class and methods
        required_methods = [
            'class FaceNavigator',
            'def load_config',
            'def save_config',
            'def calculate_eye_aspect_ratio',
            'def calibrate_face_center',
            'def move_cursor_with_face',
            'def detect_blinks',
            'def run'
        ]
        
        missing_methods = []
        for method in required_methods:
            if method in content:
                print(f"✓ {method}")
            else:
                print(f"✗ {method} - not found") 
                missing_methods.append(method)
        
        if missing_imports or missing_methods:
            return False
        
        print("\n✓ Main script structure is valid")
        return True
        
    except Exception as e:
        print(f"✗ Main script test failed: {e}")
        return False

def test_documentation():
    """Test documentation completeness"""
    print("\nTesting documentation...")
    
    try:
        # Test main README
        with open('README.md', 'r') as f:
            readme_content = f.read()
        
        required_sections = [
            'Face Navigation App',
            'Quick Start',
            'Features',
            'How It Works',
            'Usage Examples'
        ]
        
        missing_sections = []
        for section in required_sections:
            if section in readme_content:
                print(f"✓ README contains: {section}")
            else:
                print(f"✗ README missing: {section}")
                missing_sections.append(section)
        
        # Test detailed documentation
        with open('README_FaceNavigator.md', 'r') as f:
            detailed_content = f.read()
        
        detailed_sections = [
            'Installation',
            'Usage',
            'Configuration',
            'Troubleshooting'
        ]
        
        for section in detailed_sections:
            if section in detailed_content:
                print(f"✓ Detailed README contains: {section}")
            else:
                print(f"✗ Detailed README missing: {section}")
                missing_sections.append(section)
        
        if missing_sections:
            return False
        
        print("\n✓ Documentation is complete")
        return True
        
    except Exception as e:
        print(f"✗ Documentation test failed: {e}")
        return False

def main():
    """Run all validation tests"""
    print("Face Navigator - Comprehensive Validation")
    print("=" * 50)
    
    tests = [
        test_file_structure,
        test_executable_permissions,
        test_configuration,
        test_main_script,
        test_documentation
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()  # Add spacing between tests
    
    print("=" * 50)
    print(f"Validation Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All validation tests passed!")
        print("\nThe Face Navigator app is ready for use.")
        print("\nNext steps:")
        print("1. Run on Ubuntu system with webcam")
        print("2. Execute: ./install.sh")
        print("3. Execute: ./run.sh")
        return 0
    else:
        print(f"\n❌ {total - passed} test(s) failed.")
        print("Please fix the issues before deploying.")
        return 1

if __name__ == "__main__":
    sys.exit(main())