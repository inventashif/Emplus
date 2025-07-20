# Face Navigator - Ubuntu Face Tracking Mouse Control

A Python application that allows you to control your Ubuntu desktop cursor using face movement and perform mouse clicks using eye blinks.

## Features

- **Face Tracking Navigation**: Move your cursor by moving your face
- **Eye Blink Clicking**: 
  - Left eye blink = Left mouse click
  - Right eye blink = Right mouse click
- **Automatic Calibration**: Calibrates to your face position automatically
- **Configurable Settings**: Sensitivity, thresholds, and timing can be adjusted
- **Smooth Movement**: Built-in smoothing to reduce jitter
- **Background Operation**: Can run without showing video feed

## Requirements

- Ubuntu 18.04 or later
- Python 3.6+
- Webcam
- Good lighting conditions for face detection

## Installation

1. Clone or download this repository
2. Run the installation script:
   ```bash
   ./install.sh
   ```

The installation script will:
- Install system dependencies (OpenCV, dlib, etc.)
- Create a Python virtual environment
- Install Python packages
- Download facial landmark detection model

## Usage

### Quick Start
```bash
./run.sh
```

### With Video Preview (for debugging)
```bash
./run.sh --show-video
```

### Manual Execution
```bash
source venv/bin/activate
python3 face_navigator.py
```

## How It Works

1. **Calibration Phase**: 
   - Look straight ahead when starting the application
   - Keep your face steady for about 1-2 seconds
   - The app will calibrate your neutral face position

2. **Navigation**:
   - Move your face left/right to move cursor horizontally
   - Move your face up/down to move cursor vertically
   - Movement is relative to your calibrated position

3. **Clicking**:
   - Blink your left eye to perform a left click
   - Blink your right eye to perform a right click
   - There's a cooldown period between blinks to prevent accidental clicks

## Configuration

Edit `config.json` to adjust settings:

- `sensitivity`: How much cursor moves relative to face movement (default: 2.0)
- `eye_ar_threshold`: Eye aspect ratio threshold for blink detection (default: 0.25)
- `eye_ar_consecutive_frames`: Required consecutive frames below threshold (default: 3)
- `blink_cooldown`: Minimum time between blinks in seconds (default: 0.5)
- `smoothing_factor`: Cursor movement smoothing (0-1, default: 0.7)
- `movement_threshold`: Minimum movement to register (default: 10)

## Troubleshooting

### Common Issues

1. **"No module named cv2"**:
   - Make sure you activated the virtual environment: `source venv/bin/activate`
   - Reinstall dependencies: `pip install -r requirements.txt`

2. **Face not detected**:
   - Ensure good lighting
   - Position yourself directly in front of the camera
   - Check if camera is working with other applications

3. **Cursor movement too sensitive/slow**:
   - Adjust the `sensitivity` value in `config.json`
   - Higher values = more sensitive movement

4. **Accidental clicks**:
   - Increase `blink_cooldown` in `config.json`
   - Adjust `eye_ar_threshold` (higher = requires more closed eyes)

5. **Permission denied for camera**:
   - Make sure your user has access to the camera
   - Check if other applications are using the camera

### System Requirements

**Minimum Hardware**:
- 2GB RAM
- Dual-core processor
- USB webcam (720p recommended)

**Recommended Hardware**:
- 4GB RAM
- Quad-core processor
- HD webcam with good low-light performance

## Autostart (Optional)

To run Face Navigator automatically on login:

1. Copy the desktop file:
   ```bash
   cp face-navigator.desktop ~/.config/autostart/
   ```

2. Edit the paths in the desktop file to match your installation

## Safety Features

- **Failsafe**: Press Ctrl+C to stop the application
- **Screen Boundaries**: Cursor movement is constrained to screen edges
- **Blink Cooldown**: Prevents rapid accidental clicking
- **Movement Threshold**: Filters out small movements/jitter

## Privacy

- All processing is done locally on your device
- No data is transmitted over the network
- Camera feed is not recorded or saved

## Dependencies

- OpenCV: Computer vision and camera handling
- dlib: Facial landmark detection
- pyautogui: Mouse control
- NumPy: Mathematical operations
- SciPy: Distance calculations
- imutils: Image processing utilities

## License

This project is open source. Feel free to modify and distribute according to your needs.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## Support

If you encounter issues:
1. Check the troubleshooting section
2. Ensure all dependencies are installed correctly
3. Verify your camera is working
4. Check the logs for error messages