from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import UUID, uuid4


class ChunkMetadata(BaseModel):
    document_id: UUID
    chunk_id: int

class Chunk(BaseModel):
    text: str
    embedding: List[float]
    metadata: ChunkMetadata