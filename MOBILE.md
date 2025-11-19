# Mobile Deployment Guide

## Building for Android

This guide shows how to build the Stair Detector app for Android phones.

### Prerequisites

1. **Linux System** (Ubuntu 20.04+ recommended)
2. **Python 3.8+**
3. **Buildozer** - Tool for creating Android packages
4. **Android SDK/NDK** (will be installed by Buildozer)

### Installation Steps

#### 1. Install System Dependencies (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install -y python3-pip git zip unzip openjdk-17-jdk \
    autoconf libtool pkg-config zlib1g-dev libncurses5-dev \
    libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
```

#### 2. Install Python Dependencies

```bash
pip3 install buildozer cython
pip3 install -r requirements.txt
```

#### 3. Build the Android APK

```bash
# Clean build (first time or after changes)
buildozer android clean
buildozer android debug

# The APK will be created in bin/ directory
```

#### 4. Install on Android Device

```bash
# Connect your Android phone via USB with USB debugging enabled
adb install -r bin/stairdetector-1.0.0-debug.apk

# Or transfer the APK to your phone and install manually
```

### Running on Android

1. **Enable Permissions**: When you first open the app, grant Camera and other requested permissions
2. **Hold Phone Normally**: The app works best when you hold the phone in portrait mode
3. **Walk Normally**: The app will automatically detect stairs and warn you if you're looking at the phone

### App Features on Mobile

- **Real-time Camera View**: Shows what the camera sees
- **Gyroscope Detection**: Uses phone's accelerometer to detect when you're looking at the screen
- **Visual Warnings**: Large orange warning text when stairs are detected
- **Haptic Feedback**: Phone vibrates when warning is issued
- **Pause/Resume**: Ability to pause detection when not needed

### Building for iOS

Building for iOS requires a macOS system with Xcode installed:

```bash
# On macOS
pip3 install kivy-ios
toolchain build python3 kivy numpy pillow
toolchain create <YourApp> <path/to/your/app>
```

For detailed iOS instructions, visit: https://kivy.org/doc/stable/guide/packaging-ios.html

### Troubleshooting

**Camera not working:**
- Make sure Camera permission is granted in Android Settings > Apps > Stair Detector > Permissions

**Gyroscope not responding:**
- The app uses the accelerometer - make sure your device has this sensor
- Try restarting the app

**Build fails:**
- Make sure all system dependencies are installed
- Try: `buildozer android clean` and rebuild
- Check buildozer logs in `.buildozer/` directory

**App crashes on startup:**
- Check logcat: `adb logcat | grep python`
- Verify all requirements are properly included in buildozer.spec

### Testing Without Building

You can test the mobile app on desktop before building:

```bash
python mobile_app.py
```

This will open a desktop window simulating the mobile interface. Note: Real sensors won't work on desktop.

### Performance Tips

For better performance on mobile:
- The app processes frames at 10 FPS by default
- Camera frames are resized to 320x240 for faster processing
- Adjust these in `mobile_app.py` if needed

### Configuration

Edit `config.py` to adjust detection sensitivity:

```python
WARNING_CONFIDENCE_THRESHOLD = 0.7  # Lower = more sensitive
WARNING_COOLDOWN = 3.0              # Seconds between warnings
```

### App Size

Expected APK size: ~50-80 MB (includes Python, Kivy, OpenCV, and NumPy)

### Minimum Requirements

- **Android**: 5.0 (Lollipop, API 21) or higher
- **iOS**: iOS 11.0 or higher
- **Sensors**: Camera, Accelerometer (standard on all modern phones)
