import sys
import json
import cohere
import logging
import tiktoken
from typing import Optional

# src
sys.path.append("./")
from src.jarvis.domain.genai.document import Document, DocumentMetadata
from src.jarvis.domain.genai.chunk import Chunk, ChunkMetadata
from src.jarvis.infrastructure.core.config import genai_config

# logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Ingestor:
    """Ingestor class for handling data ingestion from JSON files."""
    def __init__(self, auto_ingest: Optional[bool] = False):
        self.data = []
        self.client = cohere.ClientV2(api_key=genai_config.COHERE_KEY)
        self.model = genai_config.COHERE_EMB_MODEL

        if auto_ingest:
            self.extract_data_from_json()

    def extract_data_from_json(self):
        dir_path = genai_config.DATA_DIR
        logger.info(f"Extracting data from JSON files in directory: {dir_path}")

        with open(genai_config.DATA_DIR, 'r', encoding='utf-8') as f:
            raw = json.load(f)

            for doc in raw:
                metadata = DocumentMetadata(
                    title=doc.get("title", ""),
                    author=doc.get("author", ""),
                    created_date=doc.get("created_date")
                )

                document = Document(
                    full_text=doc.get("full_text", ""),
                    chunks=[],
                    metadata=metadata
                )

                self.data.append(document)

    def chunk_generator(self, max_tokens: int = 100):
        enc = tiktoken.encoding_for_model(model_name="gpt-4o")  # Please see README.md -> Design decisions, for more information.

        for document in self.data:
            full_text = document.full_text
            tokens = enc.encode(full_text)

            for i in range(0, len(tokens), max_tokens):
                chunk_tokens = tokens[i:i + max_tokens]
                chunk_text = enc.decode(chunk_tokens)
                chunk_index = i // max_tokens

                # Get embedding for this chunk
                logger.info(f"Getting embeddings with Cohere API for the chunk {chunk_index} of the document {document.metadata.title}")
                embedding_response = self.client.embed(
                    texts=[chunk_text],
                    model=self.model,
                    input_type=genai_config.COHERE_INPUT_TYPE_INGESTOR,
                    output_dimension=genai_config.COHERE_EMB_DIMENSION,
                    embedding_types=["float"]
                )
                embedding = embedding_response.embeddings.float[0]

                chunk = Chunk(
                    text=chunk_text,
                    embedding=embedding,
                    metadata=ChunkMetadata(
                        document_id=document.metadata.document_id,
                        chunk_id=chunk_index,
                    )
                )

                document.add_chunk(chunk)

                yield chunk

if __name__ == "__main__":
    # === Ingestor ===
    ingestor = Ingestor()

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
