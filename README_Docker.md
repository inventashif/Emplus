# Docker Guide for Face Navigator

This guide explains how to run the Face Navigator application using Docker.

## Prerequisites

- Docker installed and running
- Docker Compose installed
- Camera device accessible (`/dev/video0`)
- X11 display server for GUI features (Linux)

## Quick Start

### 1. Build and Run
```bash
# Simple start
./docker-run.sh

# Force rebuild and start
./docker-run.sh --build

# Start with video preview (debug mode)
./docker-run.sh --debug
```

### 2. Using Docker Compose Directly
```bash
# Build the image
docker-compose build

# Start the application
docker-compose up face-navigator

# Start in debug mode (with video preview)
docker-compose --profile debug up face-navigator-debug
```

### 3. Manual Docker Commands
```bash
# Build the image
docker build -t face-navigator .

# Run with camera and display access
docker run -it --rm \
  --device=/dev/video0 \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
  --network host \
  face-navigator
```

## Configuration

### Environment Variables
- `DISPLAY`: X11 display for GUI features
- `QT_X11_NO_MITSHM`: Prevents X11 MIT-SHM issues

### Volumes
- `/tmp/.X11-unix`: X11 socket for display access
- `./config.json`: Application configuration (optional)
- `./shape_predictor_68_face_landmarks.dat`: Facial landmarks model (optional)

### Devices
- `/dev/video0`: Camera device access

## Docker Run Script Usage

The `docker-run.sh` script provides an easy interface:

```bash
# Start normally
./docker-run.sh start

# Start with debug video preview
./docker-run.sh --debug

# Stop the application
./docker-run.sh stop

# View logs
./docker-run.sh logs

# Open shell in container
./docker-run.sh shell

# Run tests
./docker-run.sh test

# Run validation
./docker-run.sh validate

# Rebuild image
./docker-run.sh --build
```

## Troubleshooting

### Camera Access Issues
```bash
# Check camera device
ls -la /dev/video*

# Test camera access
docker run --rm -it --device=/dev/video0 ubuntu:22.04 ls -la /dev/video0
```

### Display Issues
```bash
# Allow X11 connections
xhost +local:docker

# Check display variable
echo $DISPLAY

# Test X11 access
docker run --rm -it -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix ubuntu:22.04 xeyes
```

### Permission Issues
```bash
# Add user to video group
sudo usermod -aG video $USER
newgrp video

# Add user to docker group
sudo usermod -aG docker $USER
newgrp docker
```

### Container Debugging
```bash
# Open shell in running container
docker exec -it face-navigator-app bash

# Check container logs
docker logs face-navigator-app

# Inspect container
docker inspect face-navigator-app
```

## Advanced Usage

### Custom Configuration
```bash
# Mount custom config
docker run -v $(pwd)/my-config.json:/app/config.json face-navigator
```

### Headless Mode (No GUI)
```bash
# Run without X11 display
docker run --device=/dev/video0 face-navigator
```

### Network Isolation
```bash
# Run with custom network
docker network create face-nav-net
docker run --network face-nav-net face-navigator
```

## Performance Optimization

### Resource Limits
```yaml
# In docker-compose.yml
deploy:
  resources:
    limits:
      cpus: '1.0'
      memory: 512M
    reservations:
      cpus: '0.5'
      memory: 256M
```

### GPU Acceleration (if available)
```bash
# For NVIDIA GPUs
docker run --gpus all face-navigator
```

## Security Considerations

- Container runs as non-root user (`facenavigator`)
- Minimal privileges required
- Camera and display access only
- No network ports exposed
- Read-only configuration mounting recommended

## Development

### Building Custom Images
```dockerfile
# Extend the base image
FROM face-navigator:latest
COPY my-custom-config.json /app/config.json
```

### Debugging
```bash
# Run with debug shell
./docker-run.sh shell

# Run tests
./docker-run.sh test

# Check system compatibility
./docker-run.sh validate
```

## Cleanup

```bash
# Stop and remove containers
docker-compose down

# Remove images
docker rmi face-navigator

# Clean up system
docker system prune
```