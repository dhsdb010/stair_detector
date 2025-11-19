"""
Configuration settings for the stair detector system.
"""

# Camera settings
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480
CAMERA_FPS = 30

# Gyroscope settings
GYRO_SAMPLE_RATE = 50  # Hz
TILT_THRESHOLD_DOWN = -30  # degrees, phone tilted down
TILT_THRESHOLD_UP = 30     # degrees, phone tilted up
WALKING_TILT_RANGE = (-15, 15)  # degrees, normal walking range

# Stair detection settings
EDGE_DETECTION_THRESHOLD1 = 50
EDGE_DETECTION_THRESHOLD2 = 150
HOUGH_LINES_THRESHOLD = 100
MIN_LINE_LENGTH = 50
MAX_LINE_GAP = 10
HORIZONTAL_LINE_ANGLE_TOLERANCE = 20  # degrees from horizontal

# Warning system settings
WARNING_COOLDOWN = 3.0  # seconds between warnings
WARNING_CONFIDENCE_THRESHOLD = 0.7  # 0.0 to 1.0

# Detection modes
DETECTION_MODE_CAMERA = "camera"
DETECTION_MODE_GYRO = "gyro"
DETECTION_MODE_COMBINED = "combined"
DEFAULT_DETECTION_MODE = DETECTION_MODE_COMBINED
