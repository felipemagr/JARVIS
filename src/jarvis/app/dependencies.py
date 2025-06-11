import sys
from functools import lru_cache

# src
sys.path.append("./")
from src.jarvis.domain.search.vector_store.vector_store import VectorStore
from src.jarvis.ingestor import Ingestor
from src.jarvis.retrieval import Retrieval
import logging

# logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Singleton instances
_vector_store = None
_ingestor = None
_retrieval = None


@lru_cache()
def get_vector_store() -> VectorStore:
    """Dependency to get vector store instance."""
    global _vector_store
    if _vector_store is None:
        logger.info("Initializing VectorStore")
        _vector_store = VectorStore()
    return _vector_store

@lru_cache() 
def get_ingestor() -> Ingestor:
    """Dependency to get ingestor instance."""
    global _ingestor
    if _ingestor is None:
        logger.info("Initializing Ingestor")
        _ingestor = Ingestor()
    return _ingestor

@lru_cache()
def get_retrieval() -> Retrieval:
    """Dependency to get retrieval instance."""
    global _retrieval
    if _retrieval is None:
        logger.info("Initializing Retrieval")
        _retrieval = Retrieval(get_vector_store(), get_ingestor())
    return _retrieval

def get_vector_store_dependency():
    """FastAPI dependency function for VectorStore."""
    return get_vector_store()

def get_ingestor_dependency():
    """FastAPI dependency function for Ingestor."""
    return get_ingestor()

def get_retrieval_dependency():
    """FastAPI dependency function for Retrieval."""
    return get_retrieval()
