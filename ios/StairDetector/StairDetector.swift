//
//  StairDetector.swift
//  StairDetector
//
//  Core stair detection logic using computer vision
//

import Foundation
import CoreImage
import Vision

struct DetectionResult {
    let detected: Bool
    let confidence: Double
    let direction: String?
}

class StairDetector {
    
    private let detectionThreshold: Double = 0.7
    
    func detectStairs(in pixelBuffer: CVPixelBuffer) -> DetectionResult {
        // Create a request handler
        let requestHandler = VNImageRequestHandler(cvPixelBuffer: pixelBuffer, options: [:])
        
        // Create rectangle detection request
        let request = VNDetectRectanglesRequest()
        request.minimumAspectRatio = 0.1
        request.maximumAspectRatio = 1.0
        request.minimumSize = 0.05
        request.maximumObservations = 20
        
        do {
            try requestHandler.perform([request])
            
            guard let observations = request.results else {
                return DetectionResult(detected: false, confidence: 0.0, direction: nil)
            }
            
            return analyzeRectangles(observations)
            
        } catch {
            print("Failed to perform detection: \(error)")
            return DetectionResult(detected: false, confidence: 0.0, direction: nil)
        }
    }
    
    private func analyzeRectangles(_ observations: [VNRectangleObservation]) -> DetectionResult {
        // Filter for horizontal rectangles (stairs typically have horizontal edges)
        let horizontalRects = observations.filter { observation in
            let width = observation.boundingBox.width
            let height = observation.boundingBox.height
            return width > height * 1.5 // Horizontal aspect ratio
        }
        
        guard horizontalRects.count >= 3 else {
            return DetectionResult(detected: false, confidence: 0.0, direction: nil)
        }
        
        // Calculate confidence based on number of horizontal rectangles
        let confidence = min(Double(horizontalRects.count) / 10.0, 1.0)
        
        // Determine direction based on vertical position
        let avgY = horizontalRects.reduce(0.0) { $0 + $1.boundingBox.midY } / Double(horizontalRects.count)
        let direction = avgY > 0.5 ? "down" : "up"
        
        return DetectionResult(detected: true, confidence: confidence, direction: direction)
    }
}

class WarningSystem {
    private var lastWarningTime = Date.distantPast
    private let cooldownPeriod: TimeInterval = 3.0
    
    func shouldWarn(stairsDetected: Bool, confidence: Double, userDistracted: Bool) -> Bool {
        let now = Date()
        guard now.timeIntervalSince(lastWarningTime) >= cooldownPeriod else {
            return false
        }
        
        return stairsDetected && confidence >= 0.7 && userDistracted
    }
    
    func recordWarning() {
        lastWarningTime = Date()
    }
}
