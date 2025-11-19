# Quick Start Guide

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

## Run Example

```bash
python example.py
```

This will demonstrate the stair detector with various scenarios.

## Basic Usage

```python
from stair_detector import StairDetector

# Initialize
detector = StairDetector()

# Process camera frame with gyro data
result = detector.process_frame(
    frame=camera_frame,      # numpy array from camera
    gyro_pitch=-45           # phone tilted down (degrees)
)

# Check for warnings
if result['warning']:
    print(result['warning'])
```

## Run Tests

```bash
python -m unittest test_stair_detector.py
```

## System Architecture

```
┌─────────────────────────────────────────────────┐
│           Stair Detector System                 │
├─────────────────────────────────────────────────┤
│                                                 │
│  ┌──────────────┐      ┌──────────────┐        │
│  │   Camera     │      │  Gyroscope   │        │
│  │   Input      │      │    Input     │        │
│  └──────┬───────┘      └───────┬──────┘        │
│         │                      │               │
│         v                      v               │
│  ┌──────────────┐      ┌──────────────┐        │
│  │   Camera     │      │     Gyro     │        │
│  │  Detector    │      │   Detector   │        │
│  │              │      │              │        │
│  │ • Edge Det.  │      │ • Orientation│        │
│  │ • Line Det.  │      │ • Tilt Angle │        │
│  │ • Direction  │      │ • Risk Check │        │
│  └──────┬───────┘      └───────┬──────┘        │
│         │                      │               │
│         └──────────┬───────────┘               │
│                    v                           │
│          ┌──────────────────┐                  │
│          │ Stair Detector   │                  │
│          │  (Integration)   │                  │
│          └────────┬─────────┘                  │
│                   v                            │
│          ┌──────────────────┐                  │
│          │ Warning System   │                  │
│          │                  │                  │
│          │ • Confidence     │                  │
│          │ • Cooldown       │                  │
│          │ • Alert Gen.     │                  │
│          └────────┬─────────┘                  │
│                   v                            │
│          ┌──────────────────┐                  │
│          │   User Alert     │                  │
│          └──────────────────┘                  │
└─────────────────────────────────────────────────┘
```

## Key Components

1. **Camera Detector** - Visual stair detection
   - Uses Canny edge detection
   - Hough line transform for line detection
   - Analyzes horizontal line patterns

2. **Gyro Detector** - Orientation tracking
   - Monitors phone tilt angle
   - Detects distracted walking patterns
   - Risk assessment based on orientation

3. **Warning System** - Alert management
   - Confidence-based thresholds
   - Cooldown to prevent alert fatigue
   - Direction-specific warnings

4. **Stair Detector** - Main integration
   - Combines camera and gyro data
   - Coordinates all subsystems
   - Provides unified API

## Configuration

Edit `config.py` to customize:

```python
# Detection thresholds
WARNING_CONFIDENCE_THRESHOLD = 0.7  # 0-1
WARNING_COOLDOWN = 3.0             # seconds

# Gyro thresholds
TILT_THRESHOLD_DOWN = -30          # degrees
TILT_THRESHOLD_UP = 30             # degrees
```

## Detection Modes

- **combined** (default): Both camera and gyro
- **camera**: Visual detection only
- **gyro**: Orientation tracking only

Change mode:
```python
detector.set_detection_mode('camera')
```
