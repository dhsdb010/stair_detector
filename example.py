#!/usr/bin/env python3
"""
Example usage of the stair detector system.
Demonstrates how to use the stair detector with sample data.
"""

import numpy as np
import cv2
from stair_detector import StairDetector


def create_sample_stair_image(direction='down'):
    """
    Create a sample image with stairs for testing.
    
    Args:
        direction: 'up' or 'down' to position stairs accordingly
        
    Returns:
        Sample image as numpy array
    """
    # Create a blank image
    img = np.ones((480, 640, 3), dtype=np.uint8) * 200
    
    # Draw horizontal lines to simulate stairs
    num_steps = 5
    step_height = 30
    
    if direction == 'down':
        start_y = 300  # Lower in frame
    else:
        start_y = 100  # Higher in frame
    
    for i in range(num_steps):
        y = start_y + i * step_height
        # Draw step edge
        cv2.line(img, (100, y), (540, y), (50, 50, 50), 3)
        # Draw step surface
        if i < num_steps - 1:
            y_next = start_y + (i + 1) * step_height
            pts = np.array([[100, y], [540, y], [520, y_next], [120, y_next]], np.int32)
            cv2.fillPoly(img, [pts], (180, 180, 180))
    
    return img


def simulate_gyro_data(scenario='looking_at_phone'):
    """
    Simulate gyroscope data for different scenarios.
    
    Args:
        scenario: 'looking_at_phone', 'neutral', or 'tilted_up'
        
    Returns:
        Tuple of (pitch, roll, yaw) angles in degrees
    """
    scenarios = {
        'looking_at_phone': (-45, 0, 0),  # Phone tilted down, user looking at it
        'neutral': (0, 0, 0),              # Phone upright
        'tilted_up': (45, 0, 0),           # Phone tilted up
        'walking': (-10, 5, 0)             # Typical walking position
    }
    
    return scenarios.get(scenario, (0, 0, 0))


def main():
    """Main example function."""
    print("=" * 60)
    print("Stair Detector System - Example Usage")
    print("=" * 60)
    print()
    
    # Initialize the detector
    detector = StairDetector(detection_mode='combined')
    print(f"Initialized detector in '{detector.detection_mode}' mode")
    print()
    
    # Test scenarios
    scenarios = [
        {
            'name': 'Walking down stairs while looking at phone (DANGEROUS)',
            'image_direction': 'down',
            'gyro_scenario': 'looking_at_phone'
        },
        {
            'name': 'Walking down stairs with phone in neutral position',
            'image_direction': 'down',
            'gyro_scenario': 'neutral'
        },
        {
            'name': 'Walking up stairs while looking at phone (DANGEROUS)',
            'image_direction': 'up',
            'gyro_scenario': 'looking_at_phone'
        },
        {
            'name': 'Walking with phone up (looking ahead)',
            'image_direction': 'down',
            'gyro_scenario': 'tilted_up'
        },
        {
            'name': 'Walking normally with phone in typical position',
            'image_direction': 'down',
            'gyro_scenario': 'walking'
        }
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"Scenario {i}: {scenario['name']}")
        print("-" * 60)
        
        # Create sample data
        frame = create_sample_stair_image(scenario['image_direction'])
        pitch, roll, yaw = simulate_gyro_data(scenario['gyro_scenario'])
        
        # Process the frame
        result = detector.process_frame(frame, pitch, roll, yaw)
        
        # Display results
        print(f"  Stairs Detected: {result['stairs_detected']}")
        print(f"  Confidence: {result['confidence']:.2%}")
        print(f"  Direction: {result['direction']}")
        print(f"  User Distracted: {result['user_distracted']}")
        print(f"  Orientation: {result['orientation']}")
        print(f"  Should Warn: {result['should_warn']}")
        
        if result['warning']:
            print(f"  {result['warning']}")
        
        print()
    
    # Show system status
    print("=" * 60)
    print("System Status:")
    status = detector.get_status()
    print(f"  Detection Mode: {status['detection_mode']}")
    print(f"  Warning Active: {status['warning_status']['active']}")
    print(f"  Last Warning Type: {status['warning_status']['last_warning_type']}")
    print("=" * 60)


if __name__ == '__main__':
    main()
