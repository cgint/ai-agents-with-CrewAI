from langchain_core.language_models import BaseLanguageModel
from gemini_connect import get_llm_gemini, get_model_default_gemini, get_model_tools_gemini, get_models_gemini
from groq_connect import get_llm_groq, get_model_default_groq, get_model_tools_groq, get_models_groq
from ollama_ai_connect import get_model_default_ollama, get_model_tools_ollama, get_models_ollama, get_llm_ollama
from openrouter_connect import get_model_tools_openrouter, llm_list_openrouter, get_model_default_openrouter, get_llm_openrouter
from together_ai_connect import get_model_tools_together, llm_list_together, get_llm_together, get_model_default_together
from openai_connect import get_llm_openai, get_model_tools_openai, get_models_openai, get_model_default_openai

from langsmith import traceable
use_provider = "unset"

@traceable
def get_llm(model_name: str, temperature: float = 0.1, max_tokens: int = 1000) -> BaseLanguageModel:
    if use_provider == "openai":
        return get_llm_openai(model_name, temperature, max_tokens)
    elif use_provider == "openrouter":
        return get_llm_openrouter(model_name, temperature, max_tokens)
    elif use_provider == "together":
        return get_llm_together(model_name, temperature, max_tokens)
    elif use_provider == "ollama":
        return get_llm_ollama(model_name, temperature, max_tokens)
    elif use_provider == "groq":
        return get_llm_groq(model_name, temperature, max_tokens)
    elif use_provider == "gemini":
        return get_llm_gemini(model_name, temperature, max_tokens)
    else:
        raise ValueError(f"Unsupported provider: {use_provider}")

@traceable
def get_models() -> list[str]:
    if use_provider == "openai":
        return get_models_openai()
    elif use_provider == "openrouter":
        return llm_list_openrouter()
    elif use_provider == "together":
        return llm_list_together()
    elif use_provider == "ollama":
        return get_models_ollama()
    elif use_provider == "groq":
        return get_models_groq()
    elif use_provider == "gemini":
        return get_models_gemini()
    else:
        raise ValueError(f"Unsupported provider: {use_provider}")

@traceable
def get_model_defaults() -> tuple[str, str]:
    if use_provider == "openai":
        return get_model_default_openai(), get_model_tools_openai()
    elif use_provider == "openrouter":
        return get_model_default_openrouter(), get_model_tools_openrouter()
    elif use_provider == "together":
        return get_model_default_together(), get_model_tools_together()
    elif use_provider == "ollama":
        return get_model_default_ollama(), get_model_tools_ollama()
    elif use_provider == "groq":
        return get_model_default_groq(), get_model_tools_groq()
    elif use_provider == "gemini":
        return get_model_default_gemini(), get_model_tools_gemini()
    else:
        raise ValueError(f"Unsupported provider: {use_provider}")

