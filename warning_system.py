"""
Warning system module.
Manages alerts and warnings for stair detection.
"""

import time
from typing import Optional
import config


class WarningSystem:
    """Manages warning alerts for detected stairs."""
    
    def __init__(self):
        """Initialize the warning system."""
        self.last_warning_time = 0
        self.warning_cooldown = config.WARNING_COOLDOWN
        self.confidence_threshold = config.WARNING_CONFIDENCE_THRESHOLD
        self.warning_active = False
        self.last_warning_type = None
        
    def should_warn(self, stairs_detected: bool, confidence: float, 
                    user_distracted: bool) -> bool:
        """
        Determine if a warning should be issued.
        
        Args:
            stairs_detected: Whether stairs were detected
            confidence: Detection confidence level (0.0 to 1.0)
            user_distracted: Whether user appears distracted
            
        Returns:
            Boolean indicating if warning should be issued
        """
        current_time = time.time()
        
        # Check cooldown period
        if current_time - self.last_warning_time < self.warning_cooldown:
            return False
        
        # Only warn if stairs detected with sufficient confidence AND user is distracted
        if stairs_detected and confidence >= self.confidence_threshold and user_distracted:
            return True
            
        return False
    
    def issue_warning(self, direction: Optional[str], confidence: float) -> str:
        """
        Issue a warning and return the warning message.
        
        Args:
            direction: Stair direction ('up' or 'down')
            confidence: Detection confidence
            
        Returns:
            Warning message string
        """
        self.last_warning_time = time.time()
        self.warning_active = True
        
        if direction == 'down':
            self.last_warning_type = 'stairs_down'
            return f"⚠️  WARNING: Stairs ahead - going DOWN! Watch your step! (Confidence: {confidence:.0%})"
        elif direction == 'up':
            self.last_warning_type = 'stairs_up'
            return f"⚠️  WARNING: Stairs ahead - going UP! Watch your step! (Confidence: {confidence:.0%})"
        else:
            self.last_warning_type = 'stairs_detected'
            return f"⚠️  WARNING: Stairs detected! Watch your step! (Confidence: {confidence:.0%})"
    
    def clear_warning(self):
        """Clear the current warning state."""
        self.warning_active = False
        self.last_warning_type = None
    
    def get_warning_status(self) -> dict:
        """
        Get current warning system status.
        
        Returns:
            Dictionary with warning system state
        """
        return {
            'active': self.warning_active,
            'last_warning_type': self.last_warning_type,
            'last_warning_time': self.last_warning_time,
            'cooldown_remaining': max(0, self.warning_cooldown - (time.time() - self.last_warning_time))
        }
