"""
Camera-based stair detection module.
Uses computer vision techniques to detect stairs in camera feed.
"""

import cv2
import numpy as np
from typing import Tuple, Optional
import config


class CameraDetector:
    """Detects stairs using camera input and computer vision."""
    
    def __init__(self):
        """Initialize the camera detector."""
        self.edge_threshold1 = config.EDGE_DETECTION_THRESHOLD1
        self.edge_threshold2 = config.EDGE_DETECTION_THRESHOLD2
        self.hough_threshold = config.HOUGH_LINES_THRESHOLD
        self.min_line_length = config.MIN_LINE_LENGTH
        self.max_line_gap = config.MAX_LINE_GAP
        self.horizontal_tolerance = config.HORIZONTAL_LINE_ANGLE_TOLERANCE
        
    def detect_stairs(self, frame: np.ndarray) -> Tuple[bool, float, Optional[str]]:
        """
        Detect stairs in the given frame.
        
        Args:
            frame: Input image frame as numpy array (BGR format)
            
        Returns:
            Tuple of (stairs_detected, confidence, direction)
            - stairs_detected: Boolean indicating if stairs were detected
            - confidence: Float between 0 and 1 indicating detection confidence
            - direction: 'up', 'down', or None
        """
        if frame is None or frame.size == 0:
            return False, 0.0, None
            
        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Edge detection using Canny
        edges = cv2.Canny(blurred, self.edge_threshold1, self.edge_threshold2)
        
        # Detect lines using Hough transform
        lines = cv2.HoughLinesP(
            edges,
            rho=1,
            theta=np.pi/180,
            threshold=self.hough_threshold,
            minLineLength=self.min_line_length,
            maxLineGap=self.max_line_gap
        )
        
        if lines is None or len(lines) == 0:
            return False, 0.0, None
            
        # Analyze detected lines
        horizontal_lines = []
        for line in lines:
            x1, y1, x2, y2 = line[0]
            
            # Calculate angle
            if x2 - x1 != 0:
                angle = np.abs(np.arctan((y2 - y1) / (x2 - x1)) * 180 / np.pi)
            else:
                angle = 90
                
            # Check if line is approximately horizontal
            if angle < self.horizontal_tolerance:
                horizontal_lines.append((x1, y1, x2, y2))
        
        # Stairs typically show multiple parallel horizontal lines
        num_horizontal = len(horizontal_lines)
        
        if num_horizontal >= 3:
            # Calculate confidence based on number of horizontal lines
            confidence = min(num_horizontal / 10.0, 1.0)
            
            # Determine direction based on line positions
            # Lines lower in frame = going down, lines higher in frame = going up
            avg_y = np.mean([y1 for _, y1, _, _ in horizontal_lines])
            frame_center_y = frame.shape[0] / 2
            
            if avg_y > frame_center_y:
                direction = 'down'
            else:
                direction = 'up'
                
            return True, confidence, direction
        
        return False, 0.0, None
    
    def get_detection_visualization(self, frame: np.ndarray) -> np.ndarray:
        """
        Get a visualization of the detection process.
        
        Args:
            frame: Input image frame
            
        Returns:
            Annotated frame showing detected features
        """
        if frame is None or frame.size == 0:
            return frame
            
        # Create a copy for visualization
        vis_frame = frame.copy()
        
        # Convert to grayscale for processing
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edges = cv2.Canny(blurred, self.edge_threshold1, self.edge_threshold2)
        
        # Detect lines
        lines = cv2.HoughLinesP(
            edges,
            rho=1,
            theta=np.pi/180,
            threshold=self.hough_threshold,
            minLineLength=self.min_line_length,
            maxLineGap=self.max_line_gap
        )
        
        # Draw detected lines
        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                cv2.line(vis_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        
        return vis_frame
