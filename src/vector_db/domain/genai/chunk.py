from pydantic import BaseModel, Field
from typing import List
from uuid import UUID, uuid4


class ChunkMetadata(BaseModel):
    source: str
    page: int


class Chunk(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    text: str
    embedding: List[float]
    metadata: ChunkMetadata