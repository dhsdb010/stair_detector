"""
Main stair detector application.
Integrates camera detection, gyroscope detection, and warning system.
"""

import numpy as np
from typing import Tuple, Optional, Dict
import config
from camera_detector import CameraDetector
from gyro_detector import GyroDetector
from warning_system import WarningSystem


class StairDetector:
    """
    Main stair detection system that combines camera and gyroscope data
    to detect stairs and warn users when they are at risk.
    """
    
    def __init__(self, detection_mode: str = None):
        """
        Initialize the stair detector.
        
        Args:
            detection_mode: Detection mode ('camera', 'gyro', or 'combined')
        """
        self.detection_mode = detection_mode or config.DEFAULT_DETECTION_MODE
        self.camera_detector = CameraDetector()
        self.gyro_detector = GyroDetector()
        self.warning_system = WarningSystem()
        
    def process_frame(self, frame: np.ndarray, gyro_pitch: float, 
                     gyro_roll: float = 0.0, gyro_yaw: float = 0.0) -> Dict:
        """
        Process a single frame with sensor data.
        
        Args:
            frame: Camera frame as numpy array
            gyro_pitch: Gyroscope pitch angle in degrees
            gyro_roll: Gyroscope roll angle in degrees
            gyro_yaw: Gyroscope yaw angle in degrees
            
        Returns:
            Dictionary containing detection results and warnings
        """
        result = {
            'stairs_detected': False,
            'confidence': 0.0,
            'direction': None,
            'user_distracted': False,
            'orientation': None,
            'warning': None,
            'should_warn': False
        }
        
        # Camera-based detection
        if self.detection_mode in ['camera', 'combined']:
            stairs_detected, confidence, direction = self.camera_detector.detect_stairs(frame)
            result['stairs_detected'] = stairs_detected
            result['confidence'] = confidence
            result['direction'] = direction
        
        # Gyroscope-based detection
        if self.detection_mode in ['gyro', 'combined']:
            user_distracted, orientation = self.gyro_detector.detect_orientation(
                gyro_pitch, gyro_roll, gyro_yaw
            )
            result['user_distracted'] = user_distracted
            result['orientation'] = orientation
        
        # Combined mode - only warn if both conditions are met
        if self.detection_mode == 'combined':
            should_warn = self.warning_system.should_warn(
                result['stairs_detected'],
                result['confidence'],
                result['user_distracted']
            )
        # Camera only mode
        elif self.detection_mode == 'camera':
            should_warn = self.warning_system.should_warn(
                result['stairs_detected'],
                result['confidence'],
                True  # Always assume user might be distracted
            )
        # Gyro only mode - can't detect stairs, only orientation
        else:
            should_warn = False
        
        result['should_warn'] = should_warn
        
        # Issue warning if needed
        if should_warn:
            warning_msg = self.warning_system.issue_warning(
                result['direction'],
                result['confidence']
            )
            result['warning'] = warning_msg
        else:
            self.warning_system.clear_warning()
        
        return result
    
    def get_status(self) -> Dict:
        """
        Get current system status.
        
        Returns:
            Dictionary with system status information
        """
        return {
            'detection_mode': self.detection_mode,
            'warning_status': self.warning_system.get_warning_status()
        }
    
    def set_detection_mode(self, mode: str):
        """
        Change the detection mode.
        
        Args:
            mode: New detection mode ('camera', 'gyro', or 'combined')
        """
        valid_modes = ['camera', 'gyro', 'combined']
        if mode in valid_modes:
            self.detection_mode = mode
        else:
            raise ValueError(f"Invalid mode. Must be one of: {valid_modes}")
