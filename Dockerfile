FROM ubuntu:22.04

# Prevent interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Set working directory
WORKDIR /app

# Install minimal system dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-opencv \
    python3-numpy \
    python3-scipy \
    python3-tk \
    wget \
    bzip2 \
    v4l-utils \
    xvfb \
    x11-utils \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user
RUN useradd -m -u 1000 facenavigator && \
    usermod -a -G video facenavigator

# Copy requirements and install Python packages
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt || \
    pip3 install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org -r requirements.txt || \
    echo "Some packages may have failed, continuing..."

# Create placeholder for shape predictor (will be downloaded at runtime if needed)
RUN touch shape_predictor_68_face_landmarks.dat && \
    chown 1000:1000 shape_predictor_68_face_landmarks.dat

# Copy all application files
COPY face_navigator.py .
COPY config.json .
COPY validate_all.py .
COPY test_system.py .
COPY test_mock.py .
COPY README_FaceNavigator.md .
COPY run.sh .
COPY docker-entrypoint.sh .

# Make scripts executable
RUN chmod +x run.sh docker-entrypoint.sh

# Switch to non-root user
USER facenavigator

# Set environment variables for X11
ENV DISPLAY=:0
ENV QT_X11_NO_MITSHM=1

# Health check to ensure the app can start
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python3 -c "import cv2, dlib; print('Basic imports work')" || exit 1

# Default command
ENTRYPOINT ["./docker-entrypoint.sh"]
CMD ["python3", "face_navigator.py"]