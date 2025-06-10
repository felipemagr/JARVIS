import os
import logging

from pydantic import ConfigDict
from pydantic_settings import BaseSettings

logger = logging.getLogger(__name__)


class Config(BaseSettings):

    COMPONENT_NAME: str = "jarvis"
    COMPONENT_DESCRIPTION: str = (
        "A modular FastAPI project using Cohere embeddings and vector search."
    )
    COMPONENT_VERSION: str = "0.1.0"

    GENAI_ENVIRONMENT: str = "local"

    # Cohere Configuration
    COHERE_KEY: str = ""

    # Vector Store Configuration
    VECTORSTORE_INDEX_NAME: str = "jarvis01"
    VECTORSTORE_DIMENSION: int = 1536
    VECTORSTORE_TOP_K: int = 5
    VECTORSTORE_ALGORITHM: str = "linear"   # linear, hierarchical
    VECTORSTORE_DISTANCE: str = "euclidean"
    VECTORSTORE_INDEX_BODY: str = "vectorstore_index_body.json"
    
    # Hierarchical KNN Configuration
    VECTORSTORE_DECAY_FACTOR: float = 0.9

    model_config = ConfigDict(extra="ignore")

genai_config = Config(
    _env_file=[
        "./.env",
    ]
)
