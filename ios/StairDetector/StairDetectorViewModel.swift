//
//  StairDetectorViewModel.swift
//  StairDetector
//
//  View model managing stair detection logic
//

import Foundation
import AVFoundation
import CoreMotion
import Combine

class StairDetectorViewModel: NSObject, ObservableObject {
    // Published properties for UI updates
    @Published var isDetecting = false
    @Published var pitch: Double = 0.0
    @Published var roll: Double = 0.0
    @Published var stairsDetected = false
    @Published var direction: String? = nil
    @Published var confidence: Double = 0.0
    @Published var warningMessage: String? = nil
    @Published var previewLayer: AVCaptureVideoPreviewLayer?
    
    // Camera and motion components
    private var captureSession: AVCaptureSession?
    private var videoOutput: AVCaptureVideoDataOutput?
    private var motionManager: CMMotionManager?
    
    // Detection components
    private let stairDetector = StairDetector()
    private let warningSystem = WarningSystem()
    
    // Configuration
    private let detectionQueue = DispatchQueue(label: "com.stairdetector.detection")
    private var lastWarningTime: Date = Date.distantPast
    private let warningCooldown: TimeInterval = 3.0
    
    override init() {
        super.init()
        setupCamera()
        setupMotion()
    }
    
    // MARK: - Setup
    
    private func setupCamera() {
        captureSession = AVCaptureSession()
        captureSession?.sessionPreset = .medium
        
        guard let captureSession = captureSession else { return }
        
        // Add camera input
        guard let camera = AVCaptureDevice.default(.builtInWideAngleCamera, for: .video, position: .back) else {
            print("Failed to get camera device")
            return
        }
        
        do {
            let input = try AVCaptureDeviceInput(device: camera)
            if captureSession.canAddInput(input) {
                captureSession.addInput(input)
            }
        } catch {
            print("Failed to create camera input: \(error)")
            return
        }
        
        // Add video output
        videoOutput = AVCaptureVideoDataOutput()
        videoOutput?.setSampleBufferDelegate(self, queue: detectionQueue)
        
        if let videoOutput = videoOutput, captureSession.canAddOutput(videoOutput) {
            captureSession.addOutput(videoOutput)
        }
        
        // Create preview layer
        let previewLayer = AVCaptureVideoPreviewLayer(session: captureSession)
        previewLayer.videoGravity = .resizeAspectFill
        
        DispatchQueue.main.async {
            self.previewLayer = previewLayer
        }
    }
    
    private func setupMotion() {
        motionManager = CMMotionManager()
        motionManager?.deviceMotionUpdateInterval = 1.0 / 50.0 // 50 Hz
    }
    
    // MARK: - Control Methods
    
    func startDetection() {
        guard !isDetecting else { return }
        
        isDetecting = true
        
        // Start camera
        DispatchQueue.global(qos: .userInitiated).async { [weak self] in
            self?.captureSession?.startRunning()
        }
        
        // Start motion updates
        motionManager?.startDeviceMotionUpdates(to: .main) { [weak self] motion, error in
            guard let motion = motion else { return }
            self?.updateMotionData(motion)
        }
    }
    
    func stopDetection() {
        isDetecting = false
        
        captureSession?.stopRunning()
        motionManager?.stopDeviceMotionUpdates()
        
        DispatchQueue.main.async {
            self.warningMessage = nil
        }
    }
    
    func toggleDetection() {
        if isDetecting {
            stopDetection()
        } else {
            startDetection()
        }
    }
    
    // MARK: - Motion Updates
    
    private func updateMotionData(_ motion: CMDeviceMotion) {
        let attitude = motion.attitude
        
        // Convert to degrees
        pitch = attitude.pitch * 180.0 / .pi
        roll = attitude.roll * 180.0 / .pi
    }
    
    // MARK: - Detection Logic
    
    private func processFrame(_ sampleBuffer: CMSampleBuffer) {
        guard isDetecting else { return }
        
        // Get pixel buffer from sample buffer
        guard let pixelBuffer = CMSampleBufferGetImageBuffer(sampleBuffer) else {
            return
        }
        
        // Detect stairs in the frame
        let result = stairDetector.detectStairs(in: pixelBuffer)
        
        // Check user distraction based on pitch
        let isDistracted = pitch < -30 || (pitch >= -15 && pitch <= 15)
        
        DispatchQueue.main.async {
            self.stairsDetected = result.detected
            self.direction = result.direction
            self.confidence = result.confidence
            
            // Generate warning if necessary
            if result.detected && isDistracted && result.confidence >= 0.7 {
                let now = Date()
                if now.timeIntervalSince(self.lastWarningTime) >= self.warningCooldown {
                    self.issueWarning(direction: result.direction, confidence: result.confidence)
                    self.lastWarningTime = now
                }
            } else {
                self.warningMessage = nil
            }
        }
    }
    
    private func issueWarning(direction: String?, confidence: Double) {
        let confidencePercent = Int(confidence * 100)
        
        if let direction = direction {
            if direction == "down" {
                warningMessage = "Stairs ahead - going DOWN!\nWatch your step! (\(confidencePercent)%)"
            } else {
                warningMessage = "Stairs ahead - going UP!\nWatch your step! (\(confidencePercent)%)"
            }
        } else {
            warningMessage = "Stairs detected!\nWatch your step! (\(confidencePercent)%)"
        }
        
        // Trigger haptic feedback
        let generator = UINotificationFeedbackGenerator()
        generator.notificationOccurred(.warning)
    }
}

// MARK: - AVCaptureVideoDataOutputSampleBufferDelegate

extension StairDetectorViewModel: AVCaptureVideoDataOutputSampleBufferDelegate {
    func captureOutput(_ output: AVCaptureOutput, didOutput sampleBuffer: CMSampleBuffer, from connection: AVCaptureConnection) {
        processFrame(sampleBuffer)
    }
}
