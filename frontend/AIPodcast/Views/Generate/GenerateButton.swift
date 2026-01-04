import SwiftUI

struct GenerateButton: View {
    let isGenerating: Bool
    let onGenerate: () -> Void
    
    var body: some View {
        Button(action: onGenerate) {
            HStack {
                if isGenerating {
                    ProgressView()
                        .progressViewStyle(CircularProgressViewStyle(tint: .white))
                    Text("Generating...")
                } else {
                    Image(systemName: "waveform.circle.fill")
                    Text("Generate Podcast")
                }
            }
        }
        .buttonStyle(PrimaryButtonStyle(isEnabled: !isGenerating))
        .disabled(isGenerating)
    }
}

#Preview {
    VStack {
        GenerateButton(isGenerating: false, onGenerate: {})
        GenerateButton(isGenerating: true, onGenerate: {})
    }
    .padding()
}
