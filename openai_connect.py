from langchain_core.language_models import BaseLanguageModel
from langchain_openai import ChatOpenAI, OpenAI


def get_llm_openai(model_name: str, temperature: float = 0.1, max_tokens: int = 1000) -> BaseLanguageModel:
    if model_name.startswith("gpt-4"):
        return ChatOpenAI(model_name=model_name, temperature=temperature, max_tokens=max_tokens)
    else:
        return OpenAI(model_name=model_name, temperature=temperature, max_tokens=max_tokens)

model_gpt3_5_turbo_instruct = "gpt-3.5-turbo-instruct"
model_gpt4_0125_preview = "gpt-4-0125-preview"
model_gpt4 = "gpt-4"

def get_models_openai() -> list[str]:
    return [
            model_gpt3_5_turbo_instruct,
            model_gpt4_0125_preview,
            model_gpt4
        ]

def get_model_default_openai() -> str:
    return model_gpt3_5_turbo_instruct

def get_model_tools_openai() -> str:
    return model_gpt4

