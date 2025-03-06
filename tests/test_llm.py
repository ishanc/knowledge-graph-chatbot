import unittest
from unittest.mock import patch, MagicMock
from src.llm.mistral_client import MistralClient
from src.llm.inference import Inference

class TestLLM(unittest.TestCase):
    def setUp(self):
        self.api_key = "test_key"
        self.model_id = "test_model"
        self.mistral_client = MistralClient(self.api_key, self.model_id)
        self.inference = Inference(self.mistral_client)

    @patch('requests.post')
    def test_mistral_query(self, mock_post):
        # Mock successful API response
        mock_response = MagicMock()
        mock_response.json.return_value = [{"generated_text": "Test response"}]
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        response = self.mistral_client.query("Test prompt")
        self.assertEqual(response, "Test response")

    @patch('requests.get')
    def test_model_info(self, mock_get):
        # Mock model info response
        mock_response = MagicMock()
        mock_response.json.return_value = {"model": "test_model"}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        info = self.mistral_client.get_model_info()
        self.assertEqual(info["model"], "test_model")

    def test_batch_inference(self):
        test_inputs = ["test1", "test2"]
        with patch.object(self.mistral_client, 'query', return_value="response"):
            outputs = self.inference.batch_inference(test_inputs)
            self.assertEqual(len(outputs), len(test_inputs))

if __name__ == '__main__':
    unittest.main()