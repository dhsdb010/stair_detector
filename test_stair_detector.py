"""
Unit tests for the stair detector system.
"""

import unittest
import numpy as np
import cv2
from camera_detector import CameraDetector
from gyro_detector import GyroDetector
from warning_system import WarningSystem
from stair_detector import StairDetector


class TestCameraDetector(unittest.TestCase):
    """Test cases for camera-based stair detection."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.detector = CameraDetector()
    
    def test_empty_frame(self):
        """Test with empty frame."""
        frame = np.array([])
        detected, confidence, direction = self.detector.detect_stairs(frame)
        self.assertFalse(detected)
        self.assertEqual(confidence, 0.0)
        self.assertIsNone(direction)
    
    def test_none_frame(self):
        """Test with None frame."""
        detected, confidence, direction = self.detector.detect_stairs(None)
        self.assertFalse(detected)
        self.assertEqual(confidence, 0.0)
        self.assertIsNone(direction)
    
    def test_solid_color_frame(self):
        """Test with solid color frame (no stairs)."""
        frame = np.ones((480, 640, 3), dtype=np.uint8) * 128
        detected, confidence, direction = self.detector.detect_stairs(frame)
        self.assertFalse(detected)
    
    def test_frame_with_horizontal_lines(self):
        """Test with frame containing horizontal lines (simulated stairs)."""
        frame = np.ones((480, 640, 3), dtype=np.uint8) * 200
        
        # Draw multiple horizontal lines to simulate stairs
        for i in range(5):
            y = 200 + i * 40
            cv2.line(frame, (100, y), (540, y), (50, 50, 50), 3)
        
        detected, confidence, direction = self.detector.detect_stairs(frame)
        self.assertTrue(detected)
        self.assertGreater(confidence, 0.0)
        self.assertIn(direction, ['up', 'down'])


class TestGyroDetector(unittest.TestCase):
    """Test cases for gyroscope-based orientation detection."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.detector = GyroDetector()
    
    def test_looking_at_phone_down(self):
        """Test detection when phone is tilted down."""
        at_risk, state = self.detector.detect_orientation(-45)
        self.assertTrue(at_risk)
        self.assertEqual(state, "looking_at_phone_down")
    
    def test_phone_tilted_up(self):
        """Test detection when phone is tilted up."""
        at_risk, state = self.detector.detect_orientation(45)
        self.assertFalse(at_risk)
        self.assertEqual(state, "phone_tilted_up")
    
    def test_neutral_position(self):
        """Test detection in neutral position."""
        at_risk, state = self.detector.detect_orientation(0)
        self.assertTrue(at_risk)
        self.assertEqual(state, "walking_with_phone")
    
    def test_walking_position(self):
        """Test detection in typical walking position."""
        at_risk, state = self.detector.detect_orientation(-10)
        self.assertTrue(at_risk)
        self.assertEqual(state, "walking_with_phone")
    
    def test_is_walking_distracted(self):
        """Test distracted walking detection."""
        self.assertTrue(self.detector.is_walking_distracted(-45))
        self.assertFalse(self.detector.is_walking_distracted(45))
    
    def test_orientation_description(self):
        """Test orientation description."""
        desc = self.detector.get_orientation_description(-45)
        self.assertIsInstance(desc, str)
        self.assertGreater(len(desc), 0)


class TestWarningSystem(unittest.TestCase):
    """Test cases for warning system."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.warning_system = WarningSystem()
    
    def test_should_warn_with_high_confidence(self):
        """Test warning with high confidence and distracted user."""
        should_warn = self.warning_system.should_warn(True, 0.9, True)
        self.assertTrue(should_warn)
    
    def test_should_not_warn_low_confidence(self):
        """Test no warning with low confidence."""
        should_warn = self.warning_system.should_warn(True, 0.3, True)
        self.assertFalse(should_warn)
    
    def test_should_not_warn_user_not_distracted(self):
        """Test no warning when user is not distracted."""
        should_warn = self.warning_system.should_warn(True, 0.9, False)
        self.assertFalse(should_warn)
    
    def test_should_not_warn_no_stairs(self):
        """Test no warning when no stairs detected."""
        should_warn = self.warning_system.should_warn(False, 0.9, True)
        self.assertFalse(should_warn)
    
    def test_issue_warning_down(self):
        """Test issuing warning for stairs going down."""
        message = self.warning_system.issue_warning('down', 0.85)
        self.assertIn('DOWN', message)
        self.assertIn('85%', message)
    
    def test_issue_warning_up(self):
        """Test issuing warning for stairs going up."""
        message = self.warning_system.issue_warning('up', 0.92)
        self.assertIn('UP', message)
        self.assertIn('92%', message)
    
    def test_warning_cooldown(self):
        """Test warning cooldown period."""
        # First warning should succeed
        self.assertTrue(self.warning_system.should_warn(True, 0.9, True))
        self.warning_system.issue_warning('down', 0.9)
        
        # Second warning immediately after should fail due to cooldown
        self.assertFalse(self.warning_system.should_warn(True, 0.9, True))
    
    def test_clear_warning(self):
        """Test clearing warning state."""
        self.warning_system.issue_warning('down', 0.9)
        self.assertTrue(self.warning_system.warning_active)
        
        self.warning_system.clear_warning()
        self.assertFalse(self.warning_system.warning_active)
    
    def test_get_warning_status(self):
        """Test getting warning status."""
        status = self.warning_system.get_warning_status()
        self.assertIsInstance(status, dict)
        self.assertIn('active', status)
        self.assertIn('last_warning_type', status)


class TestStairDetector(unittest.TestCase):
    """Test cases for the integrated stair detector system."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.detector = StairDetector(detection_mode='combined')
    
    def test_initialization(self):
        """Test detector initialization."""
        self.assertEqual(self.detector.detection_mode, 'combined')
        self.assertIsNotNone(self.detector.camera_detector)
        self.assertIsNotNone(self.detector.gyro_detector)
        self.assertIsNotNone(self.detector.warning_system)
    
    def test_process_frame_combined_mode(self):
        """Test processing frame in combined mode."""
        # Create sample frame with stairs
        frame = np.ones((480, 640, 3), dtype=np.uint8) * 200
        for i in range(5):
            y = 300 + i * 40
            cv2.line(frame, (100, y), (540, y), (50, 50, 50), 3)
        
        result = self.detector.process_frame(frame, -45, 0, 0)
        
        self.assertIsInstance(result, dict)
        self.assertIn('stairs_detected', result)
        self.assertIn('confidence', result)
        self.assertIn('user_distracted', result)
        self.assertIn('warning', result)
    
    def test_camera_only_mode(self):
        """Test camera-only detection mode."""
        detector = StairDetector(detection_mode='camera')
        frame = np.ones((480, 640, 3), dtype=np.uint8) * 200
        
        result = detector.process_frame(frame, 0, 0, 0)
        self.assertEqual(detector.detection_mode, 'camera')
    
    def test_set_detection_mode(self):
        """Test changing detection mode."""
        self.detector.set_detection_mode('camera')
        self.assertEqual(self.detector.detection_mode, 'camera')
        
        self.detector.set_detection_mode('gyro')
        self.assertEqual(self.detector.detection_mode, 'gyro')
    
    def test_invalid_detection_mode(self):
        """Test setting invalid detection mode."""
        with self.assertRaises(ValueError):
            self.detector.set_detection_mode('invalid_mode')
    
    def test_get_status(self):
        """Test getting system status."""
        status = self.detector.get_status()
        self.assertIsInstance(status, dict)
        self.assertIn('detection_mode', status)
        self.assertIn('warning_status', status)


if __name__ == '__main__':
    unittest.main()
