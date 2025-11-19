"""
Gyroscope-based orientation detection module.
Detects phone orientation to determine if user is looking at phone while walking.
"""

import numpy as np
from typing import Tuple, Optional
import config


class GyroDetector:
    """Detects phone orientation using gyroscope data."""
    
    def __init__(self):
        """Initialize the gyroscope detector."""
        self.tilt_threshold_down = config.TILT_THRESHOLD_DOWN
        self.tilt_threshold_up = config.TILT_THRESHOLD_UP
        self.walking_tilt_range = config.WALKING_TILT_RANGE
        
    def detect_orientation(self, pitch: float, roll: float = 0.0, yaw: float = 0.0) -> Tuple[bool, str]:
        """
        Detect phone orientation and determine if user is at risk.
        
        Args:
            pitch: Phone pitch angle in degrees (-90 to 90)
                   Negative = tilted down, Positive = tilted up
            roll: Phone roll angle in degrees (optional)
            yaw: Phone yaw angle in degrees (optional)
            
        Returns:
            Tuple of (at_risk, orientation_state)
            - at_risk: Boolean indicating if user is looking at phone
            - orientation_state: Description of current orientation
        """
        # Check if phone is tilted in a way that suggests user is looking at it
        if pitch <= self.tilt_threshold_down:
            # Phone tilted down significantly - user likely looking at screen
            return True, "looking_at_phone_down"
        elif pitch >= self.tilt_threshold_up:
            # Phone tilted up significantly
            return False, "phone_tilted_up"
        elif self.walking_tilt_range[0] <= pitch <= self.walking_tilt_range[1]:
            # Phone in typical walking position - user might be looking at phone
            return True, "walking_with_phone"
        else:
            # Other orientations
            return False, "neutral_position"
    
    def is_walking_distracted(self, pitch: float, roll: float = 0.0) -> bool:
        """
        Determine if user is walking while distracted by phone.
        
        Args:
            pitch: Phone pitch angle in degrees
            roll: Phone roll angle in degrees
            
        Returns:
            Boolean indicating if user appears distracted
        """
        at_risk, _ = self.detect_orientation(pitch, roll)
        return at_risk
    
    def get_orientation_description(self, pitch: float) -> str:
        """
        Get a human-readable description of the phone orientation.
        
        Args:
            pitch: Phone pitch angle in degrees
            
        Returns:
            Description string
        """
        _, state = self.detect_orientation(pitch)
        
        descriptions = {
            "looking_at_phone_down": "Looking at phone (tilted down)",
            "phone_tilted_up": "Phone tilted up",
            "walking_with_phone": "Walking with phone in view",
            "neutral_position": "Phone in neutral position"
        }
        
        return descriptions.get(state, "Unknown orientation")
