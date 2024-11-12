import requests
import json
from typing import List, Dict
from ..config import settings
import logging

logger = logging.getLogger(__name__)

class OllamaService:
    def __init__(self, model_name: str = "llama3.1"):
        """
        Initialize Ollama service with a specific model.
        Default is codellama which is good for code analysis.
        """
        self.base_url = settings.ollama_url
        self.model_name = model_name

    def _make_request(self, prompt: str) -> str:
        """
        Make a request to Ollama API
        """
        url = f"{self.base_url}/api/generate"
        
        try:
            response = requests.post(url, json={
                "model": self.model_name,
                "prompt": prompt,
                "stream": False
            })
            response.raise_for_status()
            return response.json()['response']
        except requests.exceptions.RequestException as e:
            logger.error(f"Error calling Ollama API: {str(e)}")
            return json.dumps({"issues": []})

    def analyze_code(self, filename: str, content: str) -> List[Dict]:
        """
        Analyze code using Ollama
        """
        prompt = f"""
        You are a code reviewer. Analyze the following code file ({filename}) for:
        1. Code style and formatting issues
        2. Potential bugs or errors
        3. Performance improvements
        4. Best practices

        Please provide the analysis ONLY in the following JSON format without any additional text:
        {{
            "issues": [
                {{
                    "type": "style|bug|performance|best_practice",
                    "line": <line_number>,
                    "description": "<issue description>",
                    "suggestion": "<how to fix>"
                }}
            ]
        }}

        Code to analyze:
        ```
        {content}
        ```

        Remember to:
        - Be specific about line numbers
        - Provide clear descriptions
        - Give actionable suggestions
        - Return ONLY valid JSON
        """

        try:
            print("Content: ", content)
            response = self._make_request(prompt)
            # Clean up the response to ensure it's valid JSON
            response = response.strip()
            if response.startswith("```json"):
                response = response[7:]
            if response.endswith("```"):
                response = response[:-3]
            return json.loads(response)
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing Ollama response: {str(e)}")
            return {"issues": []}