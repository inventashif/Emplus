#!/usr/bin/env python3
"""
Docker Configuration Validation for Face Navigator
"""

import os
import json
import yaml
import subprocess

def test_docker_files():
    """Test Docker-related files"""
    print("Testing Docker files...")
    
    required_files = [
        'Dockerfile',
        'docker-compose.yml', 
        'docker-run.sh',
        'docker-entrypoint.sh',
        '.dockerignore',
        'README_Docker.md'
    ]
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✓ {file}")
        else:
            print(f"✗ {file} - missing")
            return False
    
    return True

def test_dockerfile():
    """Test Dockerfile syntax and content"""
    print("\nTesting Dockerfile...")
    
    try:
        with open('Dockerfile', 'r') as f:
            content = f.read()
        
        # Check for required instructions
        required_instructions = [
            'FROM ubuntu:22.04',
            'WORKDIR /app',
            'COPY requirements.txt',
            'COPY face_navigator.py',
            'USER facenavigator',
            'ENTRYPOINT'
        ]
        
        for instruction in required_instructions:
            if instruction in content:
                print(f"✓ {instruction}")
            else:
                print(f"✗ {instruction} - missing")
                return False
        
        return True
    except Exception as e:
        print(f"✗ Error reading Dockerfile: {e}")
        return False

def test_docker_compose():
    """Test docker-compose.yml syntax"""
    print("\nTesting docker-compose.yml...")
    
    try:
        with open('docker-compose.yml', 'r') as f:
            config = yaml.safe_load(f)
        
        # Check required services
        if 'services' not in config:
            print("✗ No services defined")
            return False
        
        required_services = ['face-navigator']
        for service in required_services:
            if service in config['services']:
                print(f"✓ Service: {service}")
            else:
                print(f"✗ Service: {service} - missing")
                return False
        
        # Check required configurations
        service_config = config['services']['face-navigator']
        required_configs = ['build', 'devices', 'volumes', 'environment']
        
        for config_key in required_configs:
            if config_key in service_config:
                print(f"✓ Config: {config_key}")
            else:
                print(f"✗ Config: {config_key} - missing")
                return False
        
        return True
    except Exception as e:
        print(f"✗ Error parsing docker-compose.yml: {e}")
        return False

def test_scripts():
    """Test script syntax"""
    print("\nTesting scripts...")
    
    scripts = ['docker-run.sh', 'docker-entrypoint.sh']
    
    for script in scripts:
        try:
            result = subprocess.run(['bash', '-n', script], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✓ {script} syntax")
            else:
                print(f"✗ {script} syntax error: {result.stderr}")
                return False
        except Exception as e:
            print(f"✗ Error testing {script}: {e}")
            return False
    
    return True

def test_permissions():
    """Test file permissions"""
    print("\nTesting permissions...")
    
    executable_files = ['docker-run.sh', 'docker-entrypoint.sh']
    
    for file in executable_files:
        if os.access(file, os.X_OK):
            print(f"✓ {file} - executable")
        else:
            print(f"✗ {file} - not executable")
            return False
    
    return True

def main():
    print("Face Navigator - Docker Validation")
    print("=" * 50)
    
    tests = [
        test_docker_files,
        test_dockerfile, 
        test_docker_compose,
        test_scripts,
        test_permissions
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"Docker Validation Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All Docker validation tests passed!")
        print("\nThe Face Navigator app is ready for Docker deployment.")
        print("\nNext steps:")
        print("1. Run: ./docker-run.sh --build")
        print("2. Test: ./docker-run.sh test")
        print("3. Start: ./docker-run.sh")
        return True
    else:
        print("❌ Some Docker validation tests failed!")
        return False

if __name__ == "__main__":
    exit(0 if main() else 1)