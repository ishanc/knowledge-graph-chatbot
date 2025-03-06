import numpy as np
from sentence_transformers import SentenceTransformer
from typing import Dict, List, Any
from ..core.logger import log_info, log_error
from ..core.config import HF_API_KEY

class Vectorizer:
    def __init__(self, model_name: str = 'sentence-transformers/all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(
            model_name,
            token=HF_API_KEY  # Add Hugging Face token for private models
        )
        self.vectors = {}
        self.metadata = {}

    def text_to_vector(self, text: str) -> np.ndarray:
        """Convert text to vector representation."""
        return self.model.encode(text, convert_to_numpy=True)

    def vectorize_node(self, node_id: str, node_data: Dict[str, Any]) -> bool:
        """Vectorize a single node from the knowledge graph."""
        try:
            # Combine all node attributes into a single text
            text = " ".join([f"{k}: {v}" for k, v in node_data.items()])
            vector = self.text_to_vector(text)
            self.vectors[node_id] = vector
            self.metadata[node_id] = node_data
            return True
        except Exception as e:
            log_error(f"Error vectorizing node {node_id}: {str(e)}")
            return False

    def convert_to_vector(self, graph_data: Dict[str, Any]) -> bool:
        """Convert entire knowledge graph to vector representations."""
        try:
            for node_id, attributes in graph_data['nodes'].items():
                self.vectorize_node(node_id, attributes)
            log_info("Successfully converted graph to vectors")
            return True
        except Exception as e:
            log_error(f"Error converting graph to vectors: {str(e)}")
            return False

    def get_vector(self, node_id: str) -> np.ndarray:
        """Retrieve vector for a specific node."""
        return self.vectors.get(node_id)

    def get_all_vectors(self) -> Dict[str, np.ndarray]:
        """Get all vectorized representations."""
        return self.vectors