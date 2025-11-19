"""
Stair Detector - A safety system for detecting stairs and warning distracted users.

This package provides a complete stair detection system that uses camera and
gyroscope sensors to detect stairs and warn users when they are at risk of
injury while using their phone.

Main Components:
    - CameraDetector: Visual stair detection using computer vision
    - GyroDetector: Phone orientation tracking
    - WarningSystem: Alert management
    - StairDetector: Main integration module

Example:
    >>> from stair_detector import StairDetector
    >>> detector = StairDetector()
    >>> result = detector.process_frame(camera_frame, gyro_pitch=-45)
    >>> if result['warning']:
    ...     print(result['warning'])
"""

__version__ = '1.0.0'
__author__ = 'Stair Detector Team'

from .stair_detector import StairDetector
from .camera_detector import CameraDetector
from .gyro_detector import GyroDetector
from .warning_system import WarningSystem

__all__ = [
    'StairDetector',
    'CameraDetector',
    'GyroDetector',
    'WarningSystem',
]
