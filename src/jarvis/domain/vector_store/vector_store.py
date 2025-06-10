import uuid
from typing import Dict, Any, List, Optional

# src
from jarvis.domain.search.algorithm.linear_knn import LinearKNN


class VectorStore:
    """
    A simple in-memory mock of a vector database (vectordb).

    This class simulates basic vector database functionality for testing or prototyping purposes.
    It allows storing vectors along with their associated metadata, retrieving all stored vectors and metadata,
    and checking the number of stored vectors.
    """
    def __init__(self):
        """Initialize the vector store."""
        # Dictionary to store multiple indexes
        # Structure: {index_name: {'texts': [], 'vectors': [], 'metadata': [], 'doc_ids': [], 'mappings': {}}}
        self.indexes: Dict[str, Dict[str, Any]] = {}

    def __len__(self):
        return len(self.indexes)

    def index_exists(self, index_name: str):
        """Check if an index exists

        Args:
            index_name (str): Index name
        """
        return index_name in self.indexes

    def get_all(self, index_name: str = None):
        """
        Get all texts, vectors and metadata.
        
        Args:
            index_name (str, optional): Specific index to retrieve from
        
        Returns:
            tuple: (texts, vectors, metadata)
        
        Raises:
            ValueError: If the specified index does not exist
        """
        if index_name:
            if index_name not in self.vector_store:
                raise ValueError(f"Index '{index_name}' does not exist.")
            index_data = self.vector_store[index_name]
            return (
                [doc.get("text") for doc in index_data],
                [doc.get("vector") for doc in index_data],
                [doc.get("metadata") for doc in index_data],
            )
        
        # If no index_name is specified, return from all indexes
        all_texts, all_vectors, all_metadata = [], [], []
        for index_data in self.vector_store.values():
            all_texts.extend(doc.get("text") for doc in index_data)
            all_vectors.extend(doc.get("vector") for doc in index_data)
            all_metadata.extend(doc.get("metadata") for doc in index_data)
        
        return all_texts, all_vectors, all_metadata

    def create_index(self, index_name: str, index_body: dict):
        """Create a new index

        Args:
            index_name (str): Index name
            index_body (dict): Index definition

        Example:
            # Create an index with KNN enabled for vector storage
            index_body = {
                "mappings": {
                    "properties": {
                        "text": {
                            "type": "text"
                        },
                        "metadata": {
                            "type": "object"
                        },
                        "vector_field": {
                            "type": "knn_vector",
                            "dimension": 1536,
                        },
                    }
                },
            }
        """
        if index_name in self.indexes:
            raise ValueError(f"Index '{index_name}' already exists")

        # Extract dimension from the vector field
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
            'doc_ids': [],
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
        doc: dict
    ):
        """Index a document

        Args:
            index_name (str): Index name
            doc (dict): Document to index

        Example:
            doc = {
                "text": "This is a test document",
                "metadata": {
                    "title": "Test document",
                    "author": "John Doe",
                    "date": "2021-01-01",
                },
                "vector_field": [0.1, 0.2, 0.3, ...],
            }
        """
        if index_name not in self.indexes:
            raise ValueError(f"Index '{index_name}' does not exist")
        
        # Extract vector from document
        vector = None
        metadata = {}
        doc_id = str(uuid.uuid4())  # Generate a unique ID for the document
        
        for key, value in doc.items():
            if key == 'vector_field':
                vector = value
            elif key == 'text':
                text = value
            else:
                metadata = value
        
        if vector is None:
            raise ValueError("Document must contain a 'vector_field'")
        
        # Validate vector dimension if specified
        index_data = self.indexes[index_name]
        dimension = index_data['dimension']
        if len(vector) != dimension:
            raise ValueError(f"Vector dimension {len(vector)} doesn't match document dimension {dimension}")
    
        # Store the document
        index_data = self.indexes[index_name]
        index_data['texts'].append(text)
        index_data['vectors'].append(vector)
        index_data['metadata'].append(metadata)
        index_data['doc_ids'].append(doc_id)

    def delete_document(self, index_name: str, doc_id: str):
        """Delete a document

        Args:
            index_name (str): Index name
            doc_id (str): Document ID
        """
        if index_name not in self.indexes:
            raise ValueError(f"Index '{index_name}' does not exist")
        
        index_data = self.indexes[index_name]
        try:
            idx = index_data['doc_ids'].index(doc_id)
            del index_data['texts'][idx]
            del index_data['vectors'][idx]
            del index_data['metadata'][idx]
            del index_data['doc_ids'][idx]
        except ValueError:
            raise ValueError(f"Document with ID '{doc_id}' not found")

    def query_index(self, index_name: str, query_vector: List[float], top_k: int = 5, algorithm: Optional[str] = "linear", distance: Optional[str] = "euclidean"):
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
        
        if algorithm == "linear":
            # Initialize LinearKNN with the specified distance metric
            linear_knn = LinearKNN(distance_metric=distance.lower())
            
            index_data = self.indexes[index_name]
            vectors = index_data['vectors']
            metadata = index_data['metadata']
            doc_ids = index_data['doc_ids']
            
            if not vectors:
                return []
            
            # Calculate similarities/distances using LinearKNN
            similarities = []
            for i, stored_vector in enumerate(vectors):
                # Use the LinearKNN.score() method to calculate scores
                score = linear_knn.score(query_vector, stored_vector)
                similarities.append({
                    'id': doc_ids[i],
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
