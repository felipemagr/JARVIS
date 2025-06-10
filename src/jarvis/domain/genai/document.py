from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import UUID, uuid4

# src
from jarvis.domain.genai.chunk import Chunk


class DocumentMetadata(BaseModel):
    title: str
    author: str
    created_date: Optional[str] = None

class Document(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    chunks: List[Chunk]
    metadata: DocumentMetadata
    
    def add_chunk(self, chunk: Chunk) -> None:
        """Add a chunk to this document"""
        chunk.document_id = self.id
        self.chunks.append(chunk)