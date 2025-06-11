import sys
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from typing import List

# src
sys.path.append("./")
from src.jarvis.app.api.models.requests import DocumentUploadRequest
from src.jarvis.app.api.models.responses import DocumentResponse, SuccessResponse
from src.jarvis.app.dependencies import get_vector_store_dependency, get_ingestor_dependency
from src.jarvis.app.api.services.document_service import DocumentService
from src.jarvis.domain.search.vector_store.vector_store import VectorStore
from src.jarvis.ingestor import Ingestor

router = APIRouter()

@router.post("/", response_model=SuccessResponse)
async def upload_document(
    request: DocumentUploadRequest,
    vector_store: VectorStore = Depends(get_vector_store_dependency),
    ingestor: Ingestor = Depends(get_ingestor_dependency)
):
    """Upload and index a document."""
    service = DocumentService(vector_store, ingestor)
    
    try:
        document_id = await service.upload_document(
            index_name=request.index_name,
            title=request.title,
            author=request.author,
            full_text=request.full_text,
            created_date=request.created_date
        )
        return SuccessResponse(
            success=True, 
            message=f"Document uploaded and indexed successfully with ID: {document_id}"
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{index_name}", response_model=List[DocumentResponse])
async def list_documents(
    index_name: str,
    vector_store: VectorStore = Depends(get_vector_store_dependency)
):
    """List all documents in an index."""
    if not vector_store.index_exists(index_name):
        raise HTTPException(status_code=404, detail=f"Index '{index_name}' not found")
    
    service = DocumentService(vector_store, None)
    return await service.list_documents(index_name)

@router.delete("/{index_name}/{document_id}", response_model=SuccessResponse)
async def delete_document(
    index_name: str,
    document_id: UUID,
    vector_store: VectorStore = Depends(get_vector_store_dependency)
):
    """Delete a document from an index."""
    try:
        vector_store.delete_document(index_name, document_id)
        return SuccessResponse(success=True, message=f"Document '{document_id}' deleted successfully")
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
