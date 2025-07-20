#!/bin/bash

# Face Navigator Installation Script for Ubuntu

echo "Installing Face Navigator for Ubuntu..."

# Update package list
echo "Updating package list..."
sudo apt update

# Install Python3 and pip if not already installed
echo "Installing Python3 and pip..."
sudo apt install -y python3 python3-pip python3-venv

# Install system dependencies for OpenCV and dlib
echo "Installing system dependencies..."
sudo apt install -y \
    build-essential \
    cmake \
    libopencv-dev \
    python3-opencv \
    libdlib-dev \
    python3-dev \
    libboost-python-dev \
    libboost-thread-dev \
    libgtk-3-dev \
    libavcodec-dev \
    libavformat-dev \
    libswscale-dev \
    libv4l-dev \
    libxvidcore-dev \
    libx264-dev \
    libjpeg-dev \
    libpng-dev \
    libtiff-dev \
    gfortran \
    openexr \
    libatlas-base-dev \
    libtbb2 \
    libtbb-dev \
    libdc1394-22-dev \
    libxine2-dev \
    libfaac-dev \
    libmp3lame-dev \
    libtheora-dev \
    libvorbis-dev \
    libxvidcore-dev \
    libopencore-amrnb-dev \
    libopencore-amrwb-dev \
    x264 \
    v4l-utils \
    unzip

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Installation complete!"
echo ""
echo "To run the Face Navigator:"
echo "1. Activate the virtual environment: source venv/bin/activate"
echo "2. Run the application: python3 face_navigator.py"
echo ""
echo "Optional flags:"
echo "  --show-video    Show video feed window for debugging"
echo "  --config FILE   Use custom configuration file"
echo ""
echo "Example: python3 face_navigator.py --show-video"