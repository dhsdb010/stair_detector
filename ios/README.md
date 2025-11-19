# iOS Stair Detector App

Native iOS application built with Swift and SwiftUI for detecting stairs using the iPhone's camera and gyroscope.

## Features

- 📱 **Native iOS App** built with Swift and SwiftUI
- 📷 **Real-time Camera Processing** using AVFoundation
- 🔄 **Motion Detection** using CoreMotion (accelerometer/gyroscope)
- 🔍 **Computer Vision** using Vision framework for stair detection
- ⚠️ **Visual Warnings** with SwiftUI interface
- 📳 **Haptic Feedback** using UINotificationFeedbackGenerator
- ⏸️ **Pause/Resume** detection control

## Requirements

- **Xcode** 14.0 or later
- **iOS** 15.0 or later
- **iPhone** with camera and motion sensors
- **macOS** for development

## Project Structure

```
ios/
└── StairDetector/
    ├── StairDetectorApp.swift       - App entry point
    ├── ContentView.swift             - Main UI view
    ├── StairDetectorViewModel.swift  - Business logic & state management
    ├── CameraPreviewView.swift       - Camera preview component
    ├── StairDetector.swift           - Stair detection algorithms
    └── Info.plist                    - App configuration & permissions
```

## Building the App

### Option 1: Using Xcode

1. **Open in Xcode**:
   ```bash
   cd ios
   open StairDetector.xcodeproj
   ```

2. **Configure Signing**:
   - Select the project in Xcode
   - Go to "Signing & Capabilities"
   - Select your development team
   - Choose a unique Bundle Identifier (e.g., `com.yourname.stairdetector`)

3. **Build and Run**:
   - Connect your iPhone via USB
   - Select your iPhone as the target device
   - Click the "Run" button (▶️) or press `⌘R`

### Option 2: Using Command Line

```bash
cd ios

# Build the project
xcodebuild -project StairDetector.xcodeproj \
           -scheme StairDetector \
           -configuration Debug \
           -destination 'platform=iOS,name=Your iPhone' \
           build

# Install on connected device
xcodebuild -project StairDetector.xcodeproj \
           -scheme StairDetector \
           -configuration Debug \
           -destination 'platform=iOS,name=Your iPhone' \
           install
```

## Permissions

The app requires the following permissions (configured in Info.plist):

- **Camera Access** (`NSCameraUsageDescription`): To detect stairs in real-time
- **Motion Sensors** (`NSMotionUsageDescription`): To detect phone orientation

Users will be prompted to grant these permissions on first launch.

## How It Works

### 1. Camera Processing
- Uses `AVCaptureSession` to capture video frames
- Processes frames at ~10 FPS for efficiency
- Each frame is analyzed using Vision framework

### 2. Stair Detection
- Uses `VNDetectRectanglesRequest` from Vision framework
- Filters for horizontal rectangles (characteristic of stairs)
- Requires 3+ horizontal lines for detection
- Calculates confidence based on number of detected features

### 3. Motion Tracking
- Uses `CMMotionManager` for device motion updates
- Tracks pitch (forward/backward tilt) at 50 Hz
- Detects when user is looking at phone (pitch < -30°)

### 4. Warning System
- Warns only when: stairs detected + user distracted + confidence ≥ 70%
- Implements 3-second cooldown between warnings
- Provides haptic feedback via UINotificationFeedbackGenerator
- Shows visual warnings in orange banner

## UI Layout

```
┌─────────────────────────────────┐
│      Stair Detector             │
├─────────────────────────────────┤
│                                 │
│    [Camera Preview Area]        │
│    (Real-time video feed)       │
│                                 │
├─────────────────────────────────┤
│ Status:                         │
│ Pitch: -35.2°  Stairs: down     │
│                (89%)            │
├─────────────────────────────────┤
│ ⚠️ WARNING                      │
│ Stairs ahead - going DOWN!      │
│ Watch your step! (89%)          │
│ *Haptic vibration*              │
├─────────────────────────────────┤
│                                 │
│   [  Pause Detection  ]         │
│                                 │
└─────────────────────────────────┘
```

## Code Architecture

### MVVM Pattern
- **Model**: `StairDetector`, `WarningSystem`
- **ViewModel**: `StairDetectorViewModel` (ObservableObject)
- **View**: `ContentView`, `CameraPreviewView`

### Key Classes

**StairDetectorViewModel**
- Manages camera session and motion updates
- Coordinates detection pipeline
- Publishes state changes to UI
- Handles warning logic

**StairDetector**
- Performs computer vision analysis
- Uses Vision framework for rectangle detection
- Analyzes patterns to identify stairs

**CameraPreviewView**
- UIViewRepresentable wrapper for AVCaptureVideoPreviewLayer
- Displays live camera feed in SwiftUI

## Testing

### Simulator Testing
⚠️ **Note**: The app requires a physical device with camera and motion sensors. The iOS Simulator does not support these features.

### Device Testing
1. Connect your iPhone to your Mac
2. Trust the computer on your iPhone
3. Build and run from Xcode
4. Grant camera and motion permissions when prompted
5. Walk around to test stair detection

## Customization

### Detection Sensitivity

Edit values in `StairDetectorViewModel.swift`:

```swift
private let warningCooldown: TimeInterval = 3.0  // Seconds between warnings
```

Edit values in `StairDetector.swift`:

```swift
private let detectionThreshold: Double = 0.7  // Confidence threshold (0.0-1.0)
```

### UI Customization

Modify colors, fonts, and layout in `ContentView.swift`:

```swift
.background(Color.orange)  // Warning color
.foregroundColor(.white)   // Text color
.font(.title)              // Font size
```

## Performance

- **Frame Processing**: ~10 FPS (adjustable)
- **Motion Updates**: 50 Hz
- **Battery Impact**: Moderate (camera + motion sensors)
- **Memory Usage**: ~30-50 MB typical

## Troubleshooting

**Camera not working:**
- Ensure camera permissions are granted in Settings > Privacy > Camera
- Check that device has rear camera
- Restart the app

**Motion not detected:**
- Check motion permissions in Settings > Privacy > Motion & Fitness
- Ensure device has gyroscope/accelerometer
- Restart the app

**Build errors:**
- Update Xcode to latest version
- Clean build folder (⌘⇧K)
- Check signing certificate is valid

**App crashes:**
- Check Console.app logs
- Verify iOS version is 15.0+
- Check all frameworks are linked

## Distribution

### TestFlight (Beta Testing)

1. Archive the app in Xcode
2. Upload to App Store Connect
3. Create a TestFlight build
4. Invite beta testers

### App Store Release

1. Complete app metadata in App Store Connect
2. Submit for review
3. Wait for approval
4. Release to App Store

## License

MIT License - Same as the main project

## Additional Resources

- [Apple Developer Documentation](https://developer.apple.com/documentation/)
- [SwiftUI Tutorials](https://developer.apple.com/tutorials/swiftui)
- [AVFoundation Guide](https://developer.apple.com/av-foundation/)
- [Vision Framework](https://developer.apple.com/documentation/vision)
- [CoreMotion](https://developer.apple.com/documentation/coremotion)
