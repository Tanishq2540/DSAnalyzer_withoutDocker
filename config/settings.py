from autogen_ext.models.openai import OpenAIChatCompletionClient
from config.constant import MODEL
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('GROQ_API_KEY')

GROQ_API_BASE_URL = "https://api.groq.com/openai/v1"

model_info = {
    "id": MODEL,
    "family": "llama3",
    "max_tokens": 8192,  
    "is_chat_model": True,
    "prompt_cost_per_1k_tokens": 0.0,
    "completion_cost_per_1k_tokens": 0.0,
    "vision": False,
    "function_calling": False, 
    "json_output": False,
}

def get_model_client():
    model_client = OpenAIChatCompletionClient(
        model=MODEL,
        api_key=api_key,
        base_url=GROQ_API_BASE_URL,
        model_info=model_info
    )
    return model_client
