//
//  ContentView.swift
//  StairDetector
//
//  Main view for the stair detection app
//

import SwiftUI

struct ContentView: View {
    @StateObject private var viewModel = StairDetectorViewModel()
    
    var body: some View {
        ZStack {
            Color.black.edgesIgnoringSafeArea(.all)
            
            VStack(spacing: 0) {
                // Title
                Text("Stair Detector")
                    .font(.title)
                    .fontWeight(.bold)
                    .foregroundColor(.white)
                    .padding()
                
                // Camera Preview
                CameraPreviewView(viewModel: viewModel)
                    .frame(maxWidth: .infinity)
                    .frame(height: UIScreen.main.bounds.height * 0.5)
                    .cornerRadius(12)
                    .padding(.horizontal)
                
                // Status Display
                VStack(alignment: .leading, spacing: 8) {
                    Text("Status:")
                        .font(.headline)
                        .foregroundColor(.white)
                    
                    HStack {
                        Text("Pitch:")
                            .foregroundColor(.gray)
                        Text(String(format: "%.1f°", viewModel.pitch))
                            .foregroundColor(.white)
                        
                        Spacer()
                        
                        if viewModel.stairsDetected {
                            Text("Stairs: \(viewModel.direction ?? "unknown")")
                                .foregroundColor(.yellow)
                            Text("(\(Int(viewModel.confidence * 100))%)")
                                .foregroundColor(.yellow)
                        } else {
                            Text("No stairs detected")
                                .foregroundColor(.green)
                        }
                    }
                    .font(.subheadline)
                }
                .padding()
                .background(Color.gray.opacity(0.3))
                .cornerRadius(8)
                .padding(.horizontal)
                .padding(.top, 8)
                
                // Warning Display
                if let warning = viewModel.warningMessage {
                    VStack {
                        Text("⚠️ WARNING")
                            .font(.title2)
                            .fontWeight(.bold)
                        Text(warning)
                            .font(.body)
                            .multilineTextAlignment(.center)
                    }
                    .foregroundColor(.white)
                    .padding()
                    .background(Color.orange)
                    .cornerRadius(12)
                    .padding(.horizontal)
                    .padding(.top, 8)
                }
                
                Spacer()
                
                // Control Button
                Button(action: {
                    viewModel.toggleDetection()
                }) {
                    Text(viewModel.isDetecting ? "Pause Detection" : "Resume Detection")
                        .font(.headline)
                        .foregroundColor(.white)
                        .frame(maxWidth: .infinity)
                        .padding()
                        .background(viewModel.isDetecting ? Color.red : Color.green)
                        .cornerRadius(12)
                }
                .padding(.horizontal)
                .padding(.bottom, 20)
            }
        }
        .onAppear {
            viewModel.startDetection()
        }
        .onDisappear {
            viewModel.stopDetection()
        }
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
