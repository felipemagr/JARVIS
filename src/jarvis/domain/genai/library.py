from pydantic import BaseModel, Field
from typing import List
from uuid import UUID, uuid4

# src
from jarvis.domain.genai.document import Document


class LibraryMetadata(BaseModel):
    name: str
    created_at: str


class Library(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    documents: List[Document]
    metadata: LibraryMetadata