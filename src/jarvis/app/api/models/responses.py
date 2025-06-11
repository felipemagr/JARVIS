from uuid import UUID
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class IndexInfo(BaseModel):
    name: str
    dimension: int
    document_count: int
    mappings: Dict[str, Any]

class SearchResult(BaseModel):
    id: UUID
    score: float
    text: str
    metadata: Dict[str, Any]

class SearchResponse(BaseModel):
    results: List[SearchResult]
    total_results: int
    query_time_ms: float

class DocumentChunk(BaseModel):
    chunk_id: int
    text: str

class DocumentResponse(BaseModel):
    document_id: UUID
    title: str
    author: str
    created_date: Optional[str]
    chunks: List[DocumentChunk]
    
class SuccessResponse(BaseModel):
    success: bool
    message: str
    
class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None
