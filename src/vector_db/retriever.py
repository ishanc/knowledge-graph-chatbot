import numpy as np
from typing import List, Dict, Any, Tuple
from scipy.spatial.distance import cosine
from .vectorizer import Vectorizer
from ..core.logger import log_info, log_error

class Retriever:
    def __init__(self, vectorizer: Vectorizer):
        self.vectorizer = vectorizer

    def calculate_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """Calculate cosine similarity between two vectors."""
        return 1 - cosine(vec1, vec2)

    def get_similar_nodes(self, query: str, top_k: int = 5) -> List[Tuple[str, float]]:
        """Retrieve top-k similar nodes for a given query."""
        try:
            query_vector = self.vectorizer.text_to_vector(query)
            similarities = []

            for node_id, vector in self.vectorizer.get_all_vectors().items():
                similarity = self.calculate_similarity(query_vector, vector)
                similarities.append((node_id, similarity))

            # Sort by similarity score in descending order
            similarities.sort(key=lambda x: x[1], reverse=True)
            return similarities[:top_k]

        except Exception as e:
            log_error(f"Error retrieving similar nodes: {str(e)}")
            return []

    def get_node_info(self, node_id: str) -> Dict[str, Any]:
        """Get metadata for a specific node."""
        return self.vectorizer.metadata.get(node_id, {})