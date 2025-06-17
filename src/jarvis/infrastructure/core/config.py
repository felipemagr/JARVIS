import logging

from pydantic import ConfigDict
from pydantic_settings import BaseSettings

# logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Config(BaseSettings):
    """Configuration settings for the Jarvis application."""
    COMPONENT_NAME: str = "jarvis"
    COMPONENT_DESCRIPTION: str = (
        "A modular FastAPI project using Cohere embeddings and vector search."
    )
    COMPONENT_VERSION: str = "1.1.0"

    GENAI_ENVIRONMENT: str = "local"

    # Local Configuration
    DATA_DIR: str = "./data/data.json"
    INDEX_BODY_DIR: str = "./src/jarvis/infrastructure/core/vectorstore_index_body.json"
    LOCAL_QUERY: str = "Space anomalies encountered by the Odyssey"

    # Cohere Configuration
    COHERE_KEY: str = ""
    COHERE_EMB_MODEL: str = "embed-v4.0"
    COHERE_INPUT_TYPE_INGESTOR: str = "search_document"  # Docs: # https://docs.cohere.com/v2/docs/embeddings
    COHERE_INPUT_TYPE_QUERY: str = "search_query"
    COHERE_EMB_DIMENSION: int = 1024

    # Vector Store Configuration
    VECTORSTORE_CHUNK_SIZE: int = 100
    VECTORSTORE_INDEX_NAME: str = "jarvis01"
    VECTORSTORE_TOP_K: int = 5
    VECTORSTORE_ALGORITHM: str = "linear"   # linear, hierarchical
    VECTORSTORE_DISTANCE: str = "euclidean" # euclidean, cosine
    VECTORSTORE_INDEX_BODY: str = "vectorstore_index_body.json"
    
    # Hierarchical KNN Configuration
    VECTORSTORE_DECAY_FACTOR: float = 0.9

    model_config = ConfigDict(extra="ignore")

genai_config = Config(
    _env_file=[
        "./.env",
    ]
)
