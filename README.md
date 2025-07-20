# Emplus - Ubuntu Face Navigation App

A Python application that allows you to control your Ubuntu desktop cursor using face movement and perform mouse clicks using eye blinks.

## Quick Start

1. **Install**: `./install.sh`
2. **Run**: `./run.sh`
3. **Test**: `python3 test_system.py`

## Features

- 🎯 **Face Tracking Navigation**: Move cursor by moving your face
- 👁️ **Eye Blink Clicking**: Left eye blink = left click, right eye blink = right click  
- 🎛️ **Auto Calibration**: Automatically calibrates to your face position
- ⚙️ **Configurable**: Adjust sensitivity, thresholds, and timing
- 🔧 **Background Mode**: Run without video preview for better performance

## How It Works

1. **Calibration**: Look straight ahead for 1-2 seconds when starting
2. **Navigation**: Move your face to control cursor movement
3. **Clicking**: Blink left eye for left click, right eye for right click

## Files

- `face_navigator.py` - Main application
- `install.sh` - Installation script  
- `run.sh` - Startup script
- `test_system.py` - System compatibility test
- `config.json` - Configuration settings
- `requirements.txt` - Python dependencies

## Usage Examples

```bash
# Basic usage
./run.sh

# With video preview (for debugging)
./run.sh --show-video

# Test system compatibility  
python3 test_system.py
```

See [README_FaceNavigator.md](README_FaceNavigator.md) for detailed documentation.

---

## Original Android Content

**Task hijacking mitigation for Android app.**

The AndroidManifest.xml includes `android:taskAffinity=""` to prevent task hijacking attacks.