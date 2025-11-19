# iOS Development Quick Start

## Prerequisites

- **macOS** (required for Xcode)
- **Xcode** 14.0 or later
- **iPhone** with iOS 15.0 or later
- **Apple Developer Account** (free tier sufficient for development)

## Setup Steps

### 1. Install Xcode

Download from Mac App Store or [developer.apple.com](https://developer.apple.com/xcode/)

### 2. Open Project

```bash
cd ios
open StairDetector.xcodeproj
```

### 3. Configure Signing

1. In Xcode, select the project in the navigator
2. Select the "StairDetector" target
3. Go to "Signing & Capabilities" tab
4. Under "Signing", select your Team from dropdown
5. Update Bundle Identifier if needed (e.g., `com.yourname.stairdetector`)

### 4. Connect iPhone

1. Connect your iPhone to Mac via USB
2. Unlock iPhone and trust the computer if prompted
3. In Xcode, select your iPhone from the device dropdown (top toolbar)

### 5. Build and Run

Click the "Run" button (▶️) or press `⌘R`

### 6. Trust Developer Certificate

On first run on device:
1. Go to Settings > General > VPN & Device Management
2. Trust your developer certificate
3. Return to app and launch again

## Project Structure

```
ios/StairDetector/
├── StairDetectorApp.swift       # App entry point (@main)
├── ContentView.swift             # Main UI (SwiftUI)
├── StairDetectorViewModel.swift  # Business logic (MVVM)
├── CameraPreviewView.swift       # Camera display component
├── StairDetector.swift           # Detection algorithms (Vision)
└── Info.plist                    # Permissions & config
```

## Key Technologies

- **SwiftUI**: Modern declarative UI framework
- **AVFoundation**: Camera capture and preview
- **Vision**: Computer vision (rectangle detection)
- **CoreMotion**: Gyroscope and accelerometer
- **Combine**: Reactive programming for state management

## Permissions

Configured in `Info.plist`:
- `NSCameraUsageDescription`: Camera access for stair detection
- `NSMotionUsageDescription`: Motion sensors for orientation tracking

## Common Issues

### "Developer Mode Required" (iOS 16+)

1. Go to Settings > Privacy & Security > Developer Mode
2. Enable Developer Mode
3. Restart iPhone

### Build Fails - No Code Signing

1. Ensure you're signed in with Apple ID in Xcode
2. Go to Xcode > Preferences > Accounts
3. Add your Apple ID if not present
4. Select your team in project settings

### Camera Not Working

- Check Info.plist has `NSCameraUsageDescription`
- Grant camera permission in Settings > Privacy > Camera
- Ensure using real device (simulator doesn't have camera)

## Testing

⚠️ **Physical Device Required**
- Camera and motion sensors don't work in simulator
- Must use real iPhone for testing

## Next Steps

- Customize UI colors in `ContentView.swift`
- Adjust detection sensitivity in `StairDetector.swift`
- Add app icon and launch screen
- Prepare for App Store submission

## Resources

- [Apple Developer Documentation](https://developer.apple.com/documentation/)
- [SwiftUI Tutorials](https://developer.apple.com/tutorials/swiftui)
- [AVFoundation Guide](https://developer.apple.com/av-foundation/)
