import uuid
from typing import Dict, Any, List, Optional

# src
from src.jarvis.domain.search.algorithm.linear_knn import LinearKNN
from src.jarvis.domain.search.algorithm.hierarchical_knn import HierarchicalKNN
from src.jarvis.domain.genai.document import Document


class VectorStore:
    """
    A simple in-memory mock of a vector database designed to work with Document/Chunk classes.

    This stores chunks as the primary searchable units, since they contain the embeddings.
    Documents are tracked separately for metadata and organization.
    """
    def __init__(self):
        """
        Initialize the vector store.

        Structure: {index_name: {'texts': [], 'vectors': [], 'metadata': [], 'dimension': int, 'mappings': {}}}
        """
        self.indexes: Dict[str, Dict[str, Any]] = {}

    def __len__(self):
        return len(self.indexes)

    def index_exists(self, index_name: str):
        """Check if an index exists

        Args:
            index_name (str): Index name
        """
        return index_name in self.indexes

    # TODO: Make the creation of indexes dinamic based on the index_body.
    def create_index(self, index_name: str, index_body: dict):
        """
        Create a new index for storing documents and chunks.
        
        Args:
            index_name (str): Name of the index
            index_body (dict): Index definition with mappings and configuration
            
        Example:
            index_body = {
                "mappings": {
                    "properties": {
                        "texts": {"type": "List[str]"},
                        "vectors": {"type": "List[float]"},
                        "metadata": {
                            "type": "object",
                            "properties": {
                                "document_id": {"type": "string"},
                                "title": {"type": "string"},
                                "author": {"type": "string"},
                                "chunk_source": {"type": "string"},
                                "chunk_page": {"type": "integer"},
                                "chunk_id": {"type": "string"},
                            }
                        },
                    }
                }
            }
        """
        if index_name in self.indexes:
            raise ValueError(f"Index '{index_name}' already exists")

        # Extract vector dimension from index_body mappings
        vector_props = index_body.get("mappings", {}).get("properties", {})
        dimension = None
        for _, props in vector_props.items():
            if props.get("type") == "knn_vector" and "dimension" in props:
                dimension = props["dimension"]
                break

        if dimension is None:
            raise ValueError("Index definition must include a 'knn_vector' field with a 'dimension' property.")

        self.indexes[index_name] = {
            'texts': [],
            'vectors': [],
            'metadata': [],
            'dimension': dimension,
            'mappings': index_body.get('mappings', {}),
        }

    def delete_index(self, index_name: str):
        """Delete an index

        Args:
            index_name (str): Index name
        """
        if index_name not in self.indexes:
            raise ValueError(f"Index '{index_name}' does not exist")
        del self.indexes[index_name]

    def index_document(
        self,
        index_name: str,
        document: Document
    ):
        """Index a document

        Args:
            index_name (str): Index name
            doc (Document): Document to index
        """
        if index_name not in self.indexes:
            raise ValueError(f"Index '{index_name}' does not exist")

        index_data = self.indexes[index_name]
        dimension = index_data['dimension']

        # Index each chunk in the Document separately
        for chunk in document.chunks:
            text = chunk.text
            vector = chunk.embedding
            if len(vector) != dimension:
                raise ValueError(
                    f"Vector dimension {len(vector)} doesn't match index dimension {dimension}"
                )

            # Combined metadata: document metadata + chunk metadata
            metadata = {
                "document_id": str(document.id),
                "title": document.metadata.title,
                "author": document.metadata.author,
                "chunk_source": chunk.metadata.source,
                "chunk_page": chunk.metadata.page,
                "chunk_id": str(chunk.id),
            }

            index_data['texts'].append(text)
            index_data['vectors'].append(vector)
            index_data['metadata'].append(metadata)

    def delete_document(self, index_name: str, doc_id: str):
        """
        Delete a document and all its associated chunks from the index.

        Args:
            index_name (str): The name of the index.
            doc_id (str): The ID of the document to delete.
        
        Raises:
            ValueError: If the index does not exist or the document ID is not found.
        """
        if index_name not in self.indexes:
            raise ValueError(f"Index '{index_name}' does not exist")
        
        index_data = self.indexes[index_name]

        # Find all indices where the metadata's document_id matches the requested doc_id
        idxs = [
            i for i, meta in enumerate(index_data['metadata'])
            if meta.get('document_id') == doc_id
        ]

        # If the list of indices is empty, the document was not found
        if not idxs:
            raise ValueError(f"Document with ID '{doc_id}' not found in index '{index_name}'")

        # Delete items from the lists by index, starting from the end
        # to avoid messing up the indices of subsequent items.
        for idx in sorted(idxs, reverse=True):
            del index_data['texts'][idx]
            del index_data['vectors'][idx]
            del index_data['metadata'][idx]

    def query_index(self, index_name: str, query_vector: List[float], top_k: int = 5, algorithm: Optional[str] = "linear", distance: Optional[str] = "euclidean", decay_factor: Optional[float] = 0.9):
        """
        Query an index by a query vector to find the top-k nearest neighbors.

        Args:
            index_name (str): Name of the index to query.
            query_vector (List[float]): Input query vector.
            top_k (int, optional): Number of nearest neighbors to return. Defaults to 5.
            algorithm (Optional[str], optional): Search algorithm to use (e.g., "linear"). Defaults to "linear".
            distance (Optional[str], optional): Distance or similarity metric to use ("cosine" or "euclidean"). Defaults to "euclidean".

        Returns:
            List[dict]: List of results, each result is a dictionary with the following keys:
                - id (str): Document ID.
                - score (float): Similarity or distance score.
                - metadata (dict): Document metadata (excluding vector_field).

        Raises:
            ValueError: If the specified index does not exist.
            NotImplementedError: If the specified algorithm is not implemented.
        """
        if index_name not in self.indexes:
            raise ValueError(f"Index '{index_name}' does not exist")
        
        if algorithm in {"linear", "hierarchical"}:
            # Select the appropriate KNN class
            if algorithm == "linear":
                knn = LinearKNN(distance_metric=distance.lower())
            elif algorithm == "hierarchical":
                knn = HierarchicalKNN(distance_metric=distance.lower(), decay_factor=decay_factor)
            
            index_data = self.indexes[index_name]
            vectors = index_data['vectors']
            metadata = index_data['metadata']
            
            if not vectors:
                return []
            
            # Calculate similarities/distances using LinearKNN
            similarities = []
            for i, stored_vector in enumerate(vectors):
                # Use the LinearKNN.score() method to calculate scores
                score = knn.score(query_vector, stored_vector)
                similarities.append({
                    'id': metadata[i]['document_id'],
                    'score': score,
                    'metadata': metadata[i]
                })
            
            # Sort by score
            # NOTE: For cosine similarity -> higher is better (descending)
            # NOTE: For euclidean distance -> lower is better (ascending)
            if distance.lower() == "cosine":
                similarities.sort(key=lambda x: x['score'], reverse=True)
            elif distance.lower() == "euclidean":
                similarities.sort(key=lambda x: x['score'], reverse=False)
            
            return similarities[:top_k]
        
        else:
            raise NotImplementedError(f"Algorithm '{algorithm}' is not implemented")

    def close(self):
        """Close the connection"""
        # For in-memory store, just clear data
        self.indexes.clear()
