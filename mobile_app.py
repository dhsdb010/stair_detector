"""
Mobile application for stair detection.
Uses phone's camera and gyroscope to detect stairs and warn users.
"""

import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.core.window import Window

# For Android sensors
try:
    from plyer import accelerometer, camera as plyer_camera, vibrator
    MOBILE_SENSORS_AVAILABLE = True
except ImportError:
    MOBILE_SENSORS_AVAILABLE = False
    print("Warning: Plyer not available. Mobile sensors won't work.")

import cv2
import numpy as np
from stair_detector import StairDetector
import math

kivy.require('2.0.0')


class StairDetectorApp(App):
    """Main mobile application for stair detection."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.detector = StairDetector(detection_mode='combined')
        self.camera_capture = None
        self.gyro_pitch = 0.0
        self.gyro_roll = 0.0
        self.gyro_yaw = 0.0
        self.detection_enabled = True
        self.last_warning = ""
        
    def build(self):
        """Build the UI."""
        # Set window size for mobile (will be fullscreen on actual device)
        Window.size = (360, 640)
        
        # Main layout
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Title
        title = Label(
            text='Stair Detector',
            size_hint=(1, 0.1),
            font_size='24sp',
            bold=True
        )
        layout.add_widget(title)
        
        # Camera preview
        self.camera_image = Image(size_hint=(1, 0.5))
        layout.add_widget(self.camera_image)
        
        # Status display
        self.status_label = Label(
            text='Status: Initializing...',
            size_hint=(1, 0.15),
            font_size='14sp',
            halign='center',
            valign='middle'
        )
        self.status_label.bind(size=self._update_text_size)
        layout.add_widget(self.status_label)
        
        # Warning display
        self.warning_label = Label(
            text='',
            size_hint=(1, 0.15),
            font_size='18sp',
            bold=True,
            color=(1, 0.3, 0, 1),  # Orange color
            halign='center',
            valign='middle'
        )
        self.warning_label.bind(size=self._update_text_size)
        layout.add_widget(self.warning_label)
        
        # Control buttons
        button_layout = BoxLayout(size_hint=(1, 0.1), spacing=10)
        
        self.toggle_button = Button(
            text='Pause Detection',
            on_press=self.toggle_detection
        )
        button_layout.add_widget(self.toggle_button)
        
        layout.add_widget(button_layout)
        
        # Start camera and sensors
        self.start_camera()
        if MOBILE_SENSORS_AVAILABLE:
            self.start_gyroscope()
        
        # Schedule detection updates
        Clock.schedule_interval(self.update, 1.0 / 10.0)  # 10 FPS
        
        return layout
    
    def _update_text_size(self, instance, value):
        """Update text size for proper wrapping."""
        instance.text_size = (instance.width, None)
    
    def start_camera(self):
        """Initialize camera capture."""
        try:
            # Try to use device camera (0 is usually the back camera)
            self.camera_capture = cv2.VideoCapture(0)
            if not self.camera_capture.isOpened():
                print("Warning: Could not open camera")
                self.status_label.text = "Status: Camera not available"
        except Exception as e:
            print(f"Error starting camera: {e}")
            self.status_label.text = f"Status: Camera error - {str(e)}"
    
    def start_gyroscope(self):
        """Initialize gyroscope/accelerometer."""
        try:
            accelerometer.enable()
            Clock.schedule_interval(self.update_gyro, 1.0 / 50.0)  # 50 Hz
        except Exception as e:
            print(f"Error starting gyroscope: {e}")
    
    def update_gyro(self, dt):
        """Update gyroscope readings."""
        if not MOBILE_SENSORS_AVAILABLE:
            # Simulate phone tilted down when looking at screen
            self.gyro_pitch = -30.0
            return
            
        try:
            # Get accelerometer data
            accel = accelerometer.acceleration
            if accel and len(accel) >= 3:
                x, y, z = accel[:3]
                
                # Calculate pitch and roll from accelerometer
                # Pitch: rotation around X axis (forward/backward tilt)
                # Roll: rotation around Y axis (left/right tilt)
                
                # Calculate pitch (angle from vertical)
                pitch = math.atan2(y, math.sqrt(x*x + z*z)) * 180.0 / math.pi
                roll = math.atan2(x, math.sqrt(y*y + z*z)) * 180.0 / math.pi
                
                self.gyro_pitch = pitch
                self.gyro_roll = roll
                
        except Exception as e:
            print(f"Error reading gyro: {e}")
    
    def update(self, dt):
        """Update detection and UI."""
        if not self.detection_enabled:
            return
            
        if self.camera_capture is None or not self.camera_capture.isOpened():
            self.status_label.text = "Status: Camera not available"
            return
        
        # Capture frame
        ret, frame = self.camera_capture.read()
        if not ret or frame is None:
            self.status_label.text = "Status: No camera frame"
            return
        
        # Resize for performance on mobile
        frame = cv2.resize(frame, (320, 240))
        
        # Process with stair detector
        result = self.detector.process_frame(
            frame,
            self.gyro_pitch,
            self.gyro_roll,
            self.gyro_yaw
        )
        
        # Update status
        status_text = f"Pitch: {self.gyro_pitch:.1f}° | "
        if result['stairs_detected']:
            status_text += f"Stairs: {result['direction']} ({result['confidence']:.0%})"
        else:
            status_text += "No stairs detected"
        
        self.status_label.text = f"Status: {status_text}"
        
        # Update warning
        if result['warning']:
            self.warning_label.text = result['warning']
            self.last_warning = result['warning']
            # Vibrate on warning
            if MOBILE_SENSORS_AVAILABLE:
                try:
                    vibrator.vibrate(0.5)  # Vibrate for 0.5 seconds
                except:
                    pass
        else:
            # Keep last warning visible for a moment
            if self.warning_label.text and self.warning_label.text.startswith('⚠️'):
                # Fade out gradually
                pass
            else:
                self.warning_label.text = ''
        
        # Display camera frame
        self.display_frame(frame)
    
    def display_frame(self, frame):
        """Display camera frame in UI."""
        # Convert BGR to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Flip for proper orientation
        frame_rgb = cv2.flip(frame_rgb, 0)
        
        # Convert to texture
        texture = Texture.create(size=(frame_rgb.shape[1], frame_rgb.shape[0]), colorfmt='rgb')
        texture.blit_buffer(frame_rgb.tobytes(), colorfmt='rgb', bufferfmt='ubyte')
        
        self.camera_image.texture = texture
    
    def toggle_detection(self, instance):
        """Toggle detection on/off."""
        self.detection_enabled = not self.detection_enabled
        if self.detection_enabled:
            self.toggle_button.text = 'Pause Detection'
            self.warning_label.text = ''
        else:
            self.toggle_button.text = 'Resume Detection'
            self.status_label.text = 'Status: Detection paused'
    
    def on_stop(self):
        """Cleanup when app closes."""
        if self.camera_capture:
            self.camera_capture.release()
        
        if MOBILE_SENSORS_AVAILABLE:
            try:
                accelerometer.disable()
            except:
                pass


def main():
    """Run the mobile application."""
    StairDetectorApp().run()


if __name__ == '__main__':
    main()
