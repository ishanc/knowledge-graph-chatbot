# src/llm/mistral_client.py

import requests
from typing import Dict, Any
from ..core.logger import log_info, log_error
from ..core.config import HF_API_KEY, HF_MODEL_ID, HF_API_BASE

class MistralClient:
    def __init__(self, api_key: str = HF_API_KEY, model_id: str = HF_MODEL_ID):
        self.api_key = api_key
        self.model_id = model_id
        self.api_url = f"{HF_API_BASE}{model_id}"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

    def query(self, prompt: str) -> str:
        """Query the Hugging Face hosted Mistral model."""
        try:
            payload = {
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": 150,
                    "temperature": 0.7,
                    "top_p": 0.95,
                    "return_full_text": False
                }
            }
            
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=payload
            )
            response.raise_for_status()
            
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                return result[0].get('generated_text', '')
            return ''

        except Exception as e:
            log_error(f"Error querying Hugging Face API: {str(e)}")
            return ''

    def get_model_info(self) -> Dict[str, Any]:
        """Get model information from Hugging Face."""
        try:
            response = requests.get(
                f"https://huggingface.co/api/models/{self.model_id}",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            log_error(f"Error fetching model info: {str(e)}")
            return {}