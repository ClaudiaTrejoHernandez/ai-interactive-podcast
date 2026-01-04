import SwiftUI

struct DocumentListView: View {
    // Placeholder data
    let placeholderDocuments = [
        "Java.pdf",
        "Onboarding.pdf",
        "Python.pdf"
    ]
    
    var body: some View {
        List(placeholderDocuments, id: \.self) { document in
            HStack {
                Image(systemName: "doc.text")
                    .foregroundColor(.blue)
                Text(document)
            }
        }
    }
}

#Preview {
    DocumentListView()
}
