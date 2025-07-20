#!/bin/bash

# Docker entrypoint script for Face Navigator

# Set permissions for video devices if running as root
if [ "$(id -u)" = "0" ]; then
    echo "Running as root, setting video device permissions..."
    chmod 666 /dev/video* 2>/dev/null || true
fi

# Check if running with display
if [ -z "$DISPLAY" ]; then
    echo "Warning: DISPLAY not set. GUI features may not work."
    echo "Make sure to run with: docker run -e DISPLAY=\$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix"
fi

# Check camera access
if [ ! -e /dev/video0 ]; then
    echo "Warning: Camera device /dev/video0 not found."
    echo "Make sure to run with: docker run --device=/dev/video0"
fi

# Download facial landmark predictor if not exists
if [ ! -f "shape_predictor_68_face_landmarks.dat" ]; then
    echo "Downloading facial landmark predictor..."
    wget -q https://github.com/italojs/facial-landmarks-recognition/raw/master/shape_predictor_68_face_landmarks.dat || {
        echo "Failed to download facial landmark predictor."
        echo "Please download it manually and mount it to the container."
    }
fi

# Execute the main command
exec "$@"