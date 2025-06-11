import sys
from typing import List, Optional

# src
sys.path.append("./")
from src.jarvis.app.api.models.responses import DocumentResponse, DocumentChunk
from src.jarvis.domain.search.vector_store.vector_store import VectorStore
from src.jarvis.ingestor import Ingestor
from src.jarvis.domain.genai.document import Document, DocumentMetadata
from src.jarvis.domain.genai.chunk import ChunkMetadata
import logging

# logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DocumentService:
    def __init__(self, vector_store: VectorStore, ingestor: Optional[Ingestor]):
        self.vector_store = vector_store
        self.ingestor = ingestor
    
    async def upload_document(
        self,
        index_name: str,
        title: str,
        author: str,
        full_text: str,
        created_date: Optional[str] = None
    ) -> str:
        """Upload and process a document for indexing."""
        if not self.vector_store.index_exists(index_name):
            raise ValueError(f"Index '{index_name}' does not exist")
        
        # Create document metadata
        metadata = DocumentMetadata(
            title=title,
            author=author,
            created_date=created_date
        )
        
        # Create document
        document = Document(
            full_text=full_text,
            chunks=[],
            metadata=metadata
        )
        
        # Process the document text into chunks with embeddings
        await self._process_document_chunks(document)
        
        # Index the document
        self.vector_store.index_document(index_name, document)
        
        logger.info(f"Document '{title}' indexed successfully with {len(document.chunks)} chunks")
        return document.metadata.document_id
    
    async def _process_document_chunks(self, document: Document):
        """Process document text into chunks using the ingestor logic."""
        if not self.ingestor:
            raise ValueError("Ingestor is required for document processing")
        
        # Use the ingestor's chunking logic
        # We'll create a temporary ingestor data structure
        temp_data = [document]
        original_data = self.ingestor.data
        self.ingestor.data = temp_data
        
        try:
            # Generate chunks for this document
            list(self.ingestor.chunk_generator())
        finally:
            # Restore original data
            self.ingestor.data = original_data
    
    async def list_documents(self, index_name: str) -> List[DocumentResponse]:
        """List all documents in an index."""
        if not self.vector_store.index_exists(index_name):
            raise ValueError(f"Index '{index_name}' does not exist")
        
        index_data = self.vector_store.indexes[index_name]
        texts = index_data['texts']
        metadata = index_data['metadata']
        
        # Group metadata by document_id to get unique documents
        documents = {}
        for i, meta in enumerate(metadata):
            chunk_meta = ChunkMetadata(**meta)
            doc_id = chunk_meta.document_id

            if doc_id not in documents:
                documents[doc_id] = {
                    'document_id': doc_id,
                    'title': meta.get('title', ''),
                    'author': meta.get('author', ''),
                    'created_date': meta.get('created_date'),
                    'chunks': []
                }

            chunk = DocumentChunk(
                chunk_id=chunk_meta.chunk_id,
                text=texts[i]
            )
            documents[doc_id]['chunks'].append(chunk)
        
        return [DocumentResponse(**doc) for doc in documents.values()]
