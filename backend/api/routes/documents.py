"""
Document upload routes.

TODO for backend engineer:
- Implement file upload validation
- Call document_processor service
- Return proper response
"""

from fastapi import APIRouter, UploadFile, File

router = APIRouter()

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """
    Upload and process a PDF document.
    
    TODO: Implement this endpoint
    Steps:
    1. Validate file is PDF
    2. Save to uploads directory
    3. Call document processor
    4. Return document_id and status
    
    See: services/document_processor.py
    """
    # TODO: Implement
    return {
        "message": "TODO: Implement document upload",
        "document_id": "stub_doc_123"
    }