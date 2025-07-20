#!/bin/bash

# Face Navigator Docker Setup and Run Script

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_usage() {
    echo "Usage: $0 [OPTIONS] [COMMAND]"
    echo ""
    echo "OPTIONS:"
    echo "  -h, --help           Show this help message"
    echo "  -b, --build          Force rebuild Docker image"
    echo "  -d, --debug          Run in debug mode (shows video preview)"
    echo "  --no-gui             Run without X11 display (cursor control only)"
    echo ""
    echo "COMMANDS:"
    echo "  start                Start face navigator (default)"
    echo "  stop                 Stop face navigator"
    echo "  logs                 Show logs"
    echo "  shell                Open shell in container"
    echo "  test                 Run system tests"
    echo "  validate             Run validation suite"
    echo ""
    echo "Examples:"
    echo "  $0                   # Start face navigator normally"
    echo "  $0 --build           # Rebuild and start"
    echo "  $0 --debug           # Start with video preview"
    echo "  $0 test              # Run tests"
    echo "  $0 shell             # Open interactive shell"
}

check_requirements() {
    # Check if Docker is installed
    if ! command -v docker &> /dev/null; then
        echo -e "${RED}Error: Docker is not installed${NC}"
        echo "Please install Docker first: https://docs.docker.com/get-docker/"
        exit 1
    fi

    # Check if Docker Compose is installed
    if ! command -v docker-compose &> /dev/null; then
        echo -e "${RED}Error: Docker Compose is not installed${NC}"
        echo "Please install Docker Compose first: https://docs.docker.com/compose/install/"
        exit 1
    fi

    # Check if user can run Docker
    if ! docker ps &> /dev/null; then
        echo -e "${RED}Error: Cannot run Docker commands${NC}"
        echo "Make sure Docker is running and your user is in the docker group:"
        echo "  sudo usermod -aG docker \$USER"
        echo "  newgrp docker"
        exit 1
    fi
}

check_camera() {
    if [ ! -e /dev/video0 ]; then
        echo -e "${YELLOW}Warning: Camera device /dev/video0 not found${NC}"
        echo "Make sure your camera is connected and accessible"
        return 1
    fi
    return 0
}

check_display() {
    if [ -z "$DISPLAY" ]; then
        echo -e "${YELLOW}Warning: DISPLAY environment variable not set${NC}"
        echo "GUI features may not work properly"
        return 1
    fi
    return 0
}

setup_x11_permissions() {
    # Allow X11 connections from Docker
    if command -v xhost &> /dev/null; then
        echo -e "${BLUE}Setting up X11 permissions...${NC}"
        xhost +local:docker
    else
        echo -e "${YELLOW}Warning: xhost not found, X11 display may not work${NC}"
    fi
}

# Parse command line arguments
BUILD=false
DEBUG=false
NO_GUI=false
COMMAND="start"

while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            print_usage
            exit 0
            ;;
        -b|--build)
            BUILD=true
            shift
            ;;
        -d|--debug)
            DEBUG=true
            shift
            ;;
        --no-gui)
            NO_GUI=true
            shift
            ;;
        start|stop|logs|shell|test|validate)
            COMMAND=$1
            shift
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            print_usage
            exit 1
            ;;
    esac
done

echo -e "${GREEN}Face Navigator Docker Manager${NC}"
echo "=============================="

# Check requirements
check_requirements

case $COMMAND in
    start)
        echo -e "${BLUE}Starting Face Navigator...${NC}"
        
        # Check camera and display
        check_camera
        if [ "$NO_GUI" = false ]; then
            check_display
            setup_x11_permissions
        fi
        
        # Build if requested
        if [ "$BUILD" = true ]; then
            echo -e "${BLUE}Building Docker image...${NC}"
            docker-compose build
        fi
        
        # Start the appropriate service
        if [ "$DEBUG" = true ]; then
            echo -e "${YELLOW}Starting in debug mode (with video preview)${NC}"
            docker-compose --profile debug up face-navigator-debug
        else
            echo -e "${GREEN}Starting Face Navigator${NC}"
            docker-compose up face-navigator
        fi
        ;;
        
    stop)
        echo -e "${BLUE}Stopping Face Navigator...${NC}"
        docker-compose down
        ;;
        
    logs)
        echo -e "${BLUE}Showing logs...${NC}"
        docker-compose logs -f face-navigator
        ;;
        
    shell)
        echo -e "${BLUE}Opening shell in container...${NC}"
        docker-compose run --rm face-navigator bash
        ;;
        
    test)
        echo -e "${BLUE}Running system tests...${NC}"
        docker-compose run --rm face-navigator python3 test_system.py
        ;;
        
    validate)
        echo -e "${BLUE}Running validation suite...${NC}"
        docker-compose run --rm face-navigator python3 validate_all.py
        ;;
        
    *)
        echo -e "${RED}Unknown command: $COMMAND${NC}"
        print_usage
        exit 1
        ;;
esac