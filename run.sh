#!/bin/bash

# Face Navigator Startup Script

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Please run install.sh first."
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Check if face landmark file exists, if not download it
if [ ! -f "shape_predictor_68_face_landmarks.dat" ]; then
    echo "Facial landmark predictor not found. It will be downloaded automatically."
fi

# Start the Face Navigator
echo "Starting Face Navigator..."
echo "Press Ctrl+C to stop"
echo ""
echo "Instructions:"
echo "1. Look straight ahead for 1-2 seconds to calibrate"
echo "2. Move your face to control the cursor"
echo "3. Blink left eye for left click"
echo "4. Blink right eye for right click"
echo ""

python3 face_navigator.py "$@"