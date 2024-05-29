from langchain_core.language_models import BaseLanguageModel
from langchain_google_genai import ChatGoogleGenerativeAI
import os

def get_llm_gemini(model_name: str, temperature: float = 0.1, max_tokens: int = 1000) -> BaseLanguageModel:
    return ChatGoogleGenerativeAI(model=model_name, temperature=temperature, max_output_tokens=max_tokens, google_api_key=os.getenv("GEMINI_API_KEY"))

model_gemini_15_flash_latest = "gemini-1.5-flash-latest"

def get_models_gemini() -> list[str]:
    return [
            model_gemini_15_flash_latest
        ]

def get_model_default_gemini() -> str:
    return model_gemini_15_flash_latest

def get_model_tools_gemini() -> str:
    return model_gemini_15_flash_latest

