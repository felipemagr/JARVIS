import logging
from typing import List, Dict, Any

from src.jarvis.infrastructure.core.config import genai_config

# logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Retrieval:
    """Retrieval class for handling search operations using a vector store."""
    def __init__(self, vector_store, ingestor):
        self.vector_store = vector_store
        self.ingestor = ingestor

    def search_by_text(
        self,
        index_name: str,
        query_text: str,
        top_k: int = genai_config.VECTORSTORE_TOP_K,
        algorithm: str = genai_config.VECTORSTORE_ALGORITHM,
        distance: str = genai_config.VECTORSTORE_DISTANCE,
        decay_factor: float = genai_config.VECTORSTORE_DECAY_FACTOR
    ) -> List[Dict[str, Any]]:
        """Search by converting text to vector first."""
        
        # Convert text to vector using the ingestor's embedding model
        logger.info(f"Converting query text to vector using {self.ingestor.model}")

        embedding_response = self.ingestor.client.embed(
            texts=[query_text],
            model=self.ingestor.model,
            input_type=genai_config.COHERE_INPUT_TYPE_QUERY,
            output_dimension=genai_config.COHERE_EMB_DIMENSION,
            embedding_types=["float"]
        )
        query_vector = embedding_response.embeddings.float[0]

        results = self.vector_store.query_index(
            index_name=index_name,
            query_vector=query_vector,
            top_k=top_k,
            algorithm=algorithm,
            distance=distance,
            decay_factor=decay_factor
        )

        return results
