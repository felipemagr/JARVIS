import sys
import json
import logging

# src
sys.path.append("./")
from src.jarvis.ingestor import Ingestor
from src.jarvis.domain.search.vector_store.vector_store import VectorStore
from src.jarvis.retrieval import Retrieval
from src.jarvis.infrastructure.core.config import genai_config

# logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    # === Load index config from JSON ===
    with open(genai_config.INDEX_BODY_DIR, "r") as f:
        index_body = json.load(f)

    # === Ingestor ===
    ingestor = Ingestor(auto_ingest=True)

    print(f"\n✅ Found {len(ingestor.data)} document(s) in '{genai_config.DATA_DIR}'")

    # Print document titles
    for idx, doc in enumerate(ingestor.data):
        print(f"📄 Document {idx+1}: '{doc.metadata.title}' by {doc.metadata.author}")

    # Generate chunks
    chunks = list(ingestor.chunk_generator(max_tokens=100))

    # Summary after chunking
    for idx, doc in enumerate(ingestor.data):
        print(f"\n📑 Document '{doc.metadata.title}' has {len(doc.chunks)} chunk(s).")
        for i, chunk in enumerate(doc.chunks):
            print(f"  🔹 Chunk {i}:")
            print(f"     - Text preview: {chunk.text[:60]!r}...")
            print(f"     - Embedding size: {len(chunk.embedding)}")
            print(f"     - Chunk index: {chunk.metadata.chunk_id}")
            print(f"     - Document ID: {chunk.metadata.document_id}")

    # === Vector Store Setup ===
    vector_store = VectorStore()
    index_name = "jarvis01"
    vector_store.create_index(index_name=index_name, index_body=index_body)

    # Index each document individually
    for doc in ingestor.data:
        vector_store.index_document(index_name=index_name, document=doc)
    
    # === Retrieval + Query ===
    retrieval = Retrieval(vector_store=vector_store, ingestor=ingestor)
    query = genai_config.LOCAL_QUERY
    results = retrieval.search_by_text(
        index_name=index_name,
        query_text=query,
        top_k=genai_config.VECTORSTORE_TOP_K,
        algorithm=genai_config.VECTORSTORE_ALGORITHM,
        distance=genai_config.VECTORSTORE_DISTANCE,
        decay_factor=genai_config.VECTORSTORE_DECAY_FACTOR
    )

    print("\n🔍 Search Results:")
    for r in results:
        print(f"-   ID: {r['id']}")
        print(f"   Score: {r['score']:.4f}")
        print(f"   Text: {r['text']}")
        print(f"   Metadata: {r['metadata']}")
        