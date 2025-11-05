import json, os
from .prompts import system_prompt, user_prompt
from langchain_ollama import ChatOllama
from langchain_anthropic import ChatAnthropic
from dotenv import load_dotenv

load_dotenv()

class AIModel():
    
    def __init__(self):
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        self.system_prompt = system_prompt
        self.user_prompt = user_prompt

    def chat(self):
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": self.user_prompt}
        ]
        try:
            # chat = ChatOllama(model="llama3.2")
            chat = ChatAnthropic(model="claude-haiku-4-5-20251001", api_key=self.api_key, max_retries=2)
            response = chat.invoke(messages)
            response = response.content.replace("```json", "").replace("```", "")
            result = json.loads(response)
            return result
        except Exception as err:
            return err
    
    def get_ai_data(self):
        response = self.chat()
        return response
