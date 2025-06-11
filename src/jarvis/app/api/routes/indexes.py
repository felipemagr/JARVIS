import sys
from fastapi import APIRouter, Depends, HTTPException
from typing import List

# src
sys.path.append("./")
from src.jarvis.app.api.models.requests import CreateIndexRequest
from src.jarvis.app.api.models.responses import IndexInfo, SuccessResponse
from src.jarvis.app.dependencies import get_vector_store_dependency
from src.jarvis.domain.search.vector_store.vector_store import VectorStore

router = APIRouter()

@router.post("/", response_model=SuccessResponse)
async def create_index(
    request: CreateIndexRequest,
    vector_store: VectorStore = Depends(get_vector_store_dependency)
):
    """Create a new index."""
    try:
        vector_store.create_index(request.index_name, request.index_body)
        return SuccessResponse(success=True, message=f"Index '{request.index_name}' created successfully")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[str])
async def list_indexes(
    vector_store: VectorStore = Depends(get_vector_store_dependency)
):
    """List all indexes."""
    return list(vector_store.indexes.keys())

@router.get("/{index_name}", response_model=IndexInfo)
async def get_index_info(
    index_name: str,
    vector_store: VectorStore = Depends(get_vector_store_dependency)
):
    """Get information about a specific index."""
    if not vector_store.index_exists(index_name):
        raise HTTPException(status_code=404, detail=f"Index '{index_name}' not found")
    
    index_data = vector_store.indexes[index_name]
    return IndexInfo(
        name=index_name,
        dimension=index_data['dimension'],
        document_count=len(set(meta.get('document_id') for meta in index_data['metadata'])),
        mappings=index_data['mappings']
    )

@router.delete("/{index_name}", response_model=SuccessResponse)
async def delete_index(
    index_name: str,
    vector_store: VectorStore = Depends(get_vector_store_dependency)
):
    """Delete an index."""
    try:
        vector_store.delete_index(index_name)
        return SuccessResponse(success=True, message=f"Index '{index_name}' deleted successfully")
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))