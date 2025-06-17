from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


class CreateIndexRequest(BaseModel):
    index_name: str = Field(..., description="Name of the index to create")
    index_body: Dict[str, Any] = Field(..., description="Index configuration and mappings")

class DocumentUploadRequest(BaseModel):
    index_name: str = Field(..., description="Target index name")
    title: str = Field(..., description="Document title")
    author: str = Field(..., description="Document author")
    full_text: str = Field(..., description="Full document text")
    created_date: Optional[str] = Field(None, description="Document creation date")

class SearchRequest(BaseModel):
    index_name: str = Field(..., description="Index to search")
    query_text: str = Field(..., description="Search query text")
    top_k: int = Field(default=5, ge=1, le=100, description="Number of results to return")
    algorithm: str = Field(default="linear", description="Search algorithm")
    distance: str = Field(default="cosine", description="Distance metric")
    decay_factor: Optional[float] = Field(default=0.9, description="Decay factor for hierarchical search")
    filter: Optional[Dict[str, Any]] = Field(
        default=None, 
        description="Metadata filter dictionary. Can contain 'document_id', 'title', 'author', and/or 'created_date'"
    )
