from pydantic import BaseModel
from typing import List
from uuid import UUID


class ChunkMetadata(BaseModel):
    document_id: UUID
    chunk_id: int

class Chunk(BaseModel):
    text: str
    embedding: List[float]
    metadata: ChunkMetadata