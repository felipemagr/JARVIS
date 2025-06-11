import sys
from fastapi import APIRouter, Depends, HTTPException
import time

# src
sys.path.append("./")
from src.jarvis.app.api.models.requests import SearchRequest
from src.jarvis.app.api.models.responses import SearchResponse, SearchResult
from src.jarvis.app.dependencies import get_vector_store_dependency, get_retrieval_dependency
from src.jarvis.domain.search.vector_store.vector_store import VectorStore
from src.jarvis.retrieval import Retrieval

router = APIRouter()

@router.post("/text", response_model=SearchResponse)
async def search_by_text(
    request: SearchRequest,
    vector_store: VectorStore = Depends(get_vector_store_dependency),
    retrieval: Retrieval = Depends(get_retrieval_dependency)
):
    """Search using text query (will be converted to vector)."""
    if not vector_store.index_exists(request.index_name):
        raise HTTPException(status_code=404, detail=f"Index '{request.index_name}' not found")
    
    start_time = time.time()
    try:
        results = retrieval.search_by_text(
            index_name=request.index_name,
            query_text=request.query_text,
            top_k=request.top_k,
            algorithm=request.algorithm,
            distance=request.distance,
            decay_factor=request.decay_factor
        )
        query_time_ms = (time.time() - start_time) * 1000
        
        search_results = [
            SearchResult(id=r['id'], score=r['score'], text=r['text'], metadata=r['metadata'])
            for r in results
        ]
        
        return SearchResponse(
            results=search_results,
            total_results=len(search_results),
            query_time_ms=query_time_ms
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
