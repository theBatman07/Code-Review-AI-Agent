import requests
import json
from typing import List, Dict
from ..config import settings
import logging

logger = logging.getLogger(__name__)

class OllamaService:
    def __init__(self, model_name: str = "llama3.1:8b"):
        self.base_url = settings.ollama_url
        self.model_name = model_name

    def make_request(self, prompt: str) -> str:
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
        json_format = """
        {
            "issues": [
                {
                    "type": "style|bug|performance|best_practice",
                    "line": <line_number>,
                    "description": "<issue description in one line>",
                    "suggestion": "<how to fix in one line>"
                }
            ]
        }

        Example output:
        {
            "task_id": "abc123",
            "status": "completed",
            "results": {
                "files": [
                    {
                        "name": "main.py",
                        "issues": [
                            {
                                "type": "style",
                                "line": 15,
                                "description": "Line too long",
                                "suggestion": "Break line into multiple lines"
                            },
                            {
                                "type": "bug",
                                "line": 23,
                                "description": "Potential null pointer",
                                "suggestion": "Add null check"
                            }
                        ]
                    }
                ],
                "summary": {
                    "total_files": 1,
                    "total_issues": 2,
                    "critical_issues": 1
                }
            }
        }
        """

        prompt = f"""
        You are a code reviewer. Analyze the following code file ({filename})

        REMEMBER TO NOT GIVE ANY INTRODUCTION, EXPLAINATION FOR WHY YOU CAME UP WITH SOLUTION. JUST GIVE THE JSON OUTPUT ASKED FOR

        DO NOT PROVIDE CODE. JUST SAY THERE IS ERROR AND IN ONE LINE WHAT TO CHANGE

        Code to analyze:
        {content}

        Please provide the analysis ONLY in the following JSON format:
        {json_format}

        GIVE JSON OUTPUT AS IN EXAMPLE AND NO EXTRA TEXT LIKE 'This is the JSON format', etc.
        """

        try:
            response = self.make_request(prompt)
            response = response.strip()
            if response.startswith("```json"):
                response = response[7:]
            if response.endswith("```"):
                response = response[:-3]
            return json.loads(response)
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing Ollama response: {str(e)}")
            return {"issues": []}