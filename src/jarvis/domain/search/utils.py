

def euclidean_distance(a: list[float], b: list[float]) -> float:
    """Calculate the Euclidean distance between two vectors."""
    squared_sum = 0.0
    for x, y in zip(a, b):
        squared_sum += (x - y) ** 2
    
    return squared_sum ** 0.5
    
def cosine_similarity(a: list[float], b: list[float]) -> float:
    """Calculate the cosine similarity between two vectors."""
    dot_product = sum(x * y for x, y in zip(a, b))

    norm_a = sum(x * x for x in a) ** 0.5
    norm_b = sum(y * y for y in b) ** 0.5

    denominator = norm_a * norm_b

    if denominator < 1e-10: # Fixed SonarQube warning: "Do not perform equality checks with floating point values."
        return 0.0

    return dot_product / denominator