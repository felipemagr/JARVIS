import sys
from typing import List, Optional

# src
sys.path.append("./")
from src.jarvis.domain.search.utils import euclidean_distance, cosine_similarity


class HierarchicalKNN:
    """
    Hierarchical scoring class — computes weighted similarity based on 
    dimension-wise hierarchical importance using the specified distance metric.

    Notes and limitations (with the help of internet & ChatGPT):
        - This approach presumes that earlier dimensions in the input vectors are more
        important than later ones.This assumption may not hold for all the cases. But
        let's go for the happy path and assume that it does.
        - Applying hierarchical weights before computing cosine similarity can distort
        the intended directionality, which is fundamental to cosine similarity. If the
        weights introduce directional bias, the similarity score may not reflect the
        true angular relationship between vectors.
        - The use of exponential decay (decay_factor ** i) for weighting is simple but
        may not be optimal for all scenarios. More advanced or learnable weighting
        schemes could yield better results in complex or domain-specific applications.
        - This is not a KNN algorithm in the traditional sense, as it does not involve 
        finding the k-nearest neighbors (this is done in VectorStore, following a similar
        approach as the OpenSearch native client). Instead, it simply computes the
        hierarchical weighted distance or similarity score between two vectors.
    """
    
    def __init__(self, distance_metric: str = 'euclidean', decay_factor: Optional[float] = 0.9):
        self.distance_metric = distance_metric.lower()
        self.decay_factor = decay_factor  # How much weight decreases per dimension level
    
    def _validate(self, a: List[float], b: List[float]) -> None:
        if len(a) != len(b):
            raise ValueError(f"Vector length mismatch: len(a)={len(a)} != len(b)={len(b)}")
    
    def _hierarchical_weights(self, dimension: int) -> List[float]:
        """Generate hierarchical weights where earlier dimensions have more importance."""
        weights = []
        for i in range(dimension):
            weight = self.decay_factor ** i
            weights.append(weight)
        return weights
    
    def score(self, a: List[float], b: List[float]) -> float:
        """
        Return hierarchical weighted distance/similarity between two vectors.
        Vector 'a' is treated as the query vector.
        """
        self._validate(a, b)
        
        weights = self._hierarchical_weights(len(a))
        
        # Apply hierarchical weighting to vectors
        weighted_a = [weights[i] * a[i] for i in range(len(a))]
        weighted_b = [weights[i] * b[i] for i in range(len(b))]
        
        if self.distance_metric == 'euclidean':
            return euclidean_distance(weighted_a, weighted_b)
        elif self.distance_metric == 'cosine':
            return cosine_similarity(weighted_a, weighted_b)
        else:
            raise ValueError(f"Unsupported distance metric: {self.distance_metric}")
