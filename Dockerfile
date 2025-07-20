FROM ubuntu:22.04

# Prevent interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
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
    unzip \
    wget \
    xvfb \
    x11-utils \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user
RUN useradd -m -u 1000 facenavigator && \
    usermod -a -G video facenavigator

# Copy requirements first for better Docker layer caching
COPY requirements.txt .

# Upgrade pip and install Python dependencies
RUN pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir -r requirements.txt

# Copy application files
COPY face_navigator.py .
COPY config.json .
COPY validate_all.py .
COPY test_system.py .
COPY test_mock.py .
COPY README_FaceNavigator.md .

# Copy and make scripts executable
COPY run.sh .
COPY docker-entrypoint.sh .
RUN chmod +x run.sh docker-entrypoint.sh

# Switch to non-root user
USER facenavigator

# Set environment variables for X11
ENV DISPLAY=:0
ENV QT_X11_NO_MITSHM=1

# Expose any ports if needed (none for this app)
# EXPOSE 8080

# Health check to ensure camera access
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python3 test_system.py || exit 1

# Default command
ENTRYPOINT ["./docker-entrypoint.sh"]
CMD ["python3", "face_navigator.py"]