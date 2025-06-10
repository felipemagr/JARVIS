from pydantic import BaseModel, Field
from typing import List
from uuid import UUID, uuid4

# src
from vector_db.domain.genai.chunk import Chunk


class DocumentMetadata(BaseModel):
    title: str
    author: str


class Document(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    chunks: List[Chunk]
    metadata: DocumentMetadata