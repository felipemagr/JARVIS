from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import UUID, uuid4

# src
from jarvis.domain.genai.chunk import Chunk


class DocumentMetadata(BaseModel):
    document_id: UUID = Field(default_factory=uuid4)
    title: str
    author: str
    created_date: Optional[str] = None

class Document(BaseModel):
    full_text: str
    chunks: List[Chunk]
    metadata: DocumentMetadata
    
    def add_chunk(self, chunk: Chunk) -> None:
        """Add a chunk to this document"""
        chunk.metadata.document_id = self.metadata.document_id
        self.chunks.append(chunk)

    def remove_chunk(self, chunk_id: UUID) -> None:
        """Remove a chunk from this document by its ID"""
        self.chunks = [c for c in self.chunks if c.metadata.chunk_id != chunk_id]