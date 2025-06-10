from typing import List

#src
from src.jarvis.domain.search.utils import euclidean_distance, cosine_similarity


class LinearKNN:
    """
    Pure scoring class — computes similarity or distance between two vectors
    using the specified distance metric.

    Notes and limitations:
        - This implementation is the perfect representation of brute force. This is not
        efficient nor scalable in ANY way. Thankfully I am implementing this as a proof
        of my coding abilities and not as a real-life solution... Long live LangChain !!!
        - This is not a KNN algorithm in the traditional sense, as it does not involve 
        finding the k-nearest neighbors (this is done in VectorStore, following a similar
        approach as the OpenSearch native client). Instead, it simply computes the distance 
        or similarity score between two vectors.
    """

    def __init__(self, distance_metric: str = 'euclidean'):
        self.distance_metric = distance_metric.lower()

    def _validate(self, a: List[float], b: List[float]) -> None:
        if len(a) != len(b):
            raise ValueError(f"Vector length mismatch: len(a)={len(a)} != len(b)={len(b)}")

    def score(self, a: List[float], b: List[float]) -> float:
        """
        Return the distance or similarity score between two vectors.
        """
        self._validate(a, b)

        if self.distance_metric == 'euclidean':
            return euclidean_distance(a, b)
        elif self.distance_metric == 'cosine':
            return cosine_similarity(a, b)
        else:
            raise ValueError(f"Unsupported distance metric: {self.distance_metric}")
