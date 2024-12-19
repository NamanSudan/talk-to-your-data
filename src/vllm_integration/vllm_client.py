
import requests
from .config import VLLM_CONFIG

class VLLMClient:
    def __init__(self):
        self.endpoint = VLLM_CONFIG["endpoint"]
        self.max_tokens = VLLM_CONFIG["max_tokens"]
        
    def generate_response(self, prompt: str) -> str:
        """Generate a response using vLLM server"""
        try:
            response = requests.post(
                f"{self.endpoint}/generate",
                json={
                    "prompt": prompt,
                    "max_tokens": self.max_tokens,
                    "temperature": 0.1,  # Lower temperature for SQL generation
                    "stop": [";", "\n"]  # Stop at query end
                }
            )
            response.raise_for_status()
            return response.json()["text"].strip()
        except Exception as e:
            raise Exception(f"Error generating response from vLLM: {str(e)}")
