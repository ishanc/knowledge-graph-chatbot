import unittest
import numpy as np
from src.vector_db.vectorizer import Vectorizer
from src.vector_db.retriever import Retriever

class TestVectorDB(unittest.TestCase):
    def setUp(self):
        self.vectorizer = Vectorizer()
        self.retriever = Retriever(self.vectorizer)
        self.test_text = "This is a test document"
        self.test_node_id = "test_node_1"

    def test_vectorizer_initialization(self):
        self.assertIsNotNone(self.vectorizer.model)
        self.assertEqual(len(self.vectorizer.vectors), 0)
        self.assertEqual(len(self.vectorizer.metadata), 0)

    def test_text_to_vector(self):
        vector = self.vectorizer.text_to_vector(self.test_text)
        self.assertIsInstance(vector, np.ndarray)
        self.assertTrue(len(vector.shape) == 1)  # Should be 1D array

    def test_vector_similarity(self):
        vec1 = self.vectorizer.text_to_vector("hello world")
        vec2 = self.vectorizer.text_to_vector("hello earth")
        similarity = self.retriever.calculate_similarity(vec1, vec2)
        self.assertIsInstance(similarity, float)
        self.assertTrue(0 <= similarity <= 1)

    def test_node_vectorization(self):
        test_data = {"text": "test content", "type": "document"}
        success = self.vectorizer.vectorize_node(self.test_node_id, test_data)
        self.assertTrue(success)
        self.assertIn(self.test_node_id, self.vectorizer.vectors)
        self.assertIn(self.test_node_id, self.vectorizer.metadata)

if __name__ == '__main__':
    unittest.main()