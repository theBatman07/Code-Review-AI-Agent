import google.generativeai as genai
from typing import List, Dict
from ..config import settings

class GeminiService:
    def __init__(self):
        genai.configure(api_key=settings.gemini_api_key)
        self.model = genai.GenerativeModel('gemini-pro')

    def analyze_code(self, filename: str, content: str) -> List[Dict]:
        prompt = f"""
        Analyze the following code file ({filename}) for:
        1. Code style and formatting issues
        2. Potential bugs or errors
        3. Performance improvements
        4. Best practices

        Provide the analysis in the following JSON format:
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
        """

        response = self.model.generate_content(prompt)
        try:
            return response.text
        except Exception as e:
            return {"issues": []}