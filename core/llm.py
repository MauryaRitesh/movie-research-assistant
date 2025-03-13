import os
from groq import Groq
from typing import Optional

class LLMClient:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        
        if not self.api_key:
            raise ValueError("Groq API Key must be set in environment variables")
            
        self.client = Groq(api_key=self.api_key)
        self.model = "llama3-70b-8192"
    
    def set_model(self, model_name: str):
        self.model = model_name
    
    def generate_response(self, prompt: str, context: Optional[str] = None) -> str:
        try:
            system_prompt = """You are a helpful research assistant with access to search tools. 
            You provide accurate information based on search results."""
            
            if context:
                system_prompt += f"\n\nHere is additional context from searches:\n{context}"
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000
            )
            
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating response: {str(e)}"