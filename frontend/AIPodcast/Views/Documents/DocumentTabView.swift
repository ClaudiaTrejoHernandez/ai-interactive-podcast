import SwiftUI

struct DocumentTabView: View {
    var body: some View {
        if #available(iOS 16.0, *) {
            NavigationStack {
                DocumentListView()
                    .navigationTitle("Documents")
            }
        } else {
            NavigationView {
                DocumentListView()
                    .navigationTitle("Documents")
            }
        }
    }
}

#Preview {
    DocumentTabView()
}
