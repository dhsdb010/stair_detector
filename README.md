# Stair Detector

A safety system that uses camera and gyroscope sensors to detect stairs and warn users when they are at risk of injury while using their phone.

## Overview

While using a phone when walking, users might not notice stairs and could be in a dangerous position due to their attention being focused on the phone screen. This can cause serious injuries. The Stair Detector uses a combination of:

- **Camera-based detection**: Computer vision to identify stairs in the camera feed
- **Gyroscope-based detection**: Phone orientation to determine if the user is looking at their phone
- **Warning system**: Alerts users when stairs are detected while they appear distracted

## Features

- Real-time stair detection using edge detection and Hough line transforms
- Phone orientation tracking to identify distracted walking
- Intelligent warning system with cooldown to prevent alert fatigue
- Multiple detection modes: camera-only, gyro-only, or combined
- Configurable sensitivity and thresholds
- Confidence-based warnings

## Installation

### Prerequisites

- Python 3.7 or higher
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone https://github.com/dhsdb010/stair_detector.git
cd stair_detector
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Quick Start

Run the example script to see the system in action:

```bash
python example.py
```

This will simulate various scenarios including:
- Walking down stairs while looking at phone (dangerous)
- Walking with phone in neutral position
- Walking up stairs while distracted
- Walking with phone in safe positions

### Programmatic Usage

```python
from stair_detector import StairDetector
import numpy as np

# Initialize the detector
detector = StairDetector(detection_mode='combined')

# Process a frame with sensor data
frame = camera.capture()  # Your camera frame
gyro_pitch = -45  # Phone tilted down (degrees)

result = detector.process_frame(frame, gyro_pitch)

if result['warning']:
    print(result['warning'])
```

## Architecture

The system consists of four main modules:

### 1. Camera Detector (`camera_detector.py`)
- Detects stairs using computer vision techniques
- Uses Canny edge detection and Hough line transforms
- Identifies horizontal lines characteristic of stairs
- Determines stair direction (up/down)

### 2. Gyroscope Detector (`gyro_detector.py`)
- Monitors phone orientation using gyroscope data
- Detects when user is looking at phone screen
- Identifies distracted walking patterns

### 3. Warning System (`warning_system.py`)
- Manages alert generation and delivery
- Implements cooldown periods to prevent alert fatigue
- Confidence-based warning thresholds

### 4. Stair Detector (`stair_detector.py`)
- Main integration module
- Combines camera and gyroscope data
- Coordinates between all subsystems

## Detection Modes

The system supports three detection modes:

1. **Combined Mode** (default): Uses both camera and gyroscope
   - Most accurate and safe
   - Only warns when stairs are detected AND user appears distracted

2. **Camera Only**: Uses only visual detection
   - Useful when gyroscope data is unavailable
   - Assumes user might always be distracted

3. **Gyro Only**: Uses only orientation detection
   - Limited utility (can't detect stairs)
   - Useful for orientation monitoring only

## Configuration

Edit `config.py` to customize detection parameters:

```python
# Camera settings
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480

# Gyroscope thresholds
TILT_THRESHOLD_DOWN = -30  # degrees
TILT_THRESHOLD_UP = 30     # degrees

# Warning settings
WARNING_COOLDOWN = 3.0  # seconds
WARNING_CONFIDENCE_THRESHOLD = 0.7  # 0.0 to 1.0
```

## Testing

Run the test suite:

```bash
python -m unittest test_stair_detector.py
```

The test suite covers:
- Camera detection accuracy
- Gyroscope orientation detection
- Warning system logic
- Integration testing

## API Reference

### StairDetector

Main class for stair detection.

**Methods:**

- `__init__(detection_mode='combined')`: Initialize detector
- `process_frame(frame, gyro_pitch, gyro_roll=0.0, gyro_yaw=0.0)`: Process sensor data
- `get_status()`: Get current system status
- `set_detection_mode(mode)`: Change detection mode

**Parameters for process_frame:**

- `frame`: numpy array (BGR format from camera)
- `gyro_pitch`: float, pitch angle in degrees (-90 to 90)
- `gyro_roll`: float, roll angle in degrees (optional)
- `gyro_yaw`: float, yaw angle in degrees (optional)

**Returns:**

Dictionary with:
- `stairs_detected`: bool
- `confidence`: float (0.0 to 1.0)
- `direction`: 'up', 'down', or None
- `user_distracted`: bool
- `orientation`: string describing phone position
- `warning`: warning message string or None
- `should_warn`: bool

## How It Works

### Stair Detection Algorithm

1. **Preprocessing**: Convert frame to grayscale and apply Gaussian blur
2. **Edge Detection**: Use Canny edge detector to find edges
3. **Line Detection**: Apply Hough line transform to find straight lines
4. **Line Analysis**: Filter for horizontal lines (characteristic of stairs)
5. **Confidence Calculation**: Based on number of parallel horizontal lines
6. **Direction Determination**: Based on vertical position in frame

### Orientation Detection

1. **Pitch Analysis**: Check phone tilt angle
2. **Risk Assessment**: Determine if user is looking at screen
3. **Pattern Recognition**: Identify distracted walking patterns

### Warning Logic

Warnings are issued when:
- Stairs are detected with confidence ≥ threshold (default 70%)
- User appears distracted (phone tilted toward face)
- Not in cooldown period (default 3 seconds)

## Safety Considerations

⚠️ **Important**: This is a prototype/demonstration system. For production use:

- Use higher-quality camera and sensor inputs
- Implement more sophisticated computer vision algorithms
- Add machine learning models for improved accuracy
- Consider haptic feedback in addition to visual warnings
- Test extensively in real-world conditions
- Comply with safety standards and regulations

## Future Enhancements

Potential improvements:
- Machine learning-based stair detection
- Integration with smartphone sensors
- Haptic and audio warnings
- Depth sensing for improved accuracy
- Multi-staircase pattern recognition
- Night/low-light detection
- Real-time performance optimization

## License

MIT License - See LICENSE file for details

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.

## Acknowledgments

This system was developed to address the real safety concern of distracted walking, particularly on stairs where injuries are common.
