import sys
import logging
from typing import List, Dict, Any

# src
sys.path.append("./")
from src.jarvis.domain.search.vector_store.vector_store import VectorStore
from src.jarvis.ingestor import Ingestor
from src.jarvis.retrieval import Retrieval
from src.jarvis.infrastructure.core.config import genai_config

# logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SearchService:
    def __init__(self, vector_store: VectorStore, ingestor: Ingestor):
        # Initialize the existing Retrieval class instead of duplicating logic
        self.retrieval = Retrieval(vector_store, ingestor)
    
    async def search_by_text(
        self,
        index_name: str,
        query_text: str,
        top_k: int = genai_config.VECTORSTORE_TOP_K,
        algorithm: str = genai_config.VECTORSTORE_ALGORITHM,
        distance: str = genai_config.VECTORSTORE_DISTANCE,
        decay_factor: float = genai_config.VECTORSTORE_DECAY_FACTOR
    ) -> List[Dict[str, Any]]:
        """Search by delegating to the existing Retrieval class."""
        
        # Delegate to your existing Retrieval class
        # Note: If your Retrieval.search_by_text is not async, we can call it directly
        # since the async wrapper doesn't add value if the underlying method is sync
        return self.retrieval.search_by_text(
            index_name=index_name,
            query_text=query_text,
            top_k=top_k,
            algorithm=algorithm,
            distance=distance,
            decay_factor=decay_factor
        )