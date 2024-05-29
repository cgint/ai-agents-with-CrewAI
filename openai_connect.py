from langchain_core.language_models import BaseLanguageModel
from langchain_openai import ChatOpenAI, OpenAI


def get_llm_openai(model_name: str, temperature: float = 0.1, max_tokens: int = 1000) -> BaseLanguageModel:
    if model_name.startswith("gpt-4"):
        return ChatOpenAI(model_name=model_name, temperature=temperature, max_tokens=max_tokens)
    else:
        return OpenAI(model_name=model_name, temperature=temperature, max_tokens=max_tokens)

model_gpt3_5_turbo_instruct = "gpt-3.5-turbo-instruct"
model_gpt4o_0513_preview = "gpt-4o-2024-05-13"
model_gpt4o = "gpt-4o"

def get_models_openai() -> list[str]:
    return [
            model_gpt3_5_turbo_instruct,
            model_gpt4o_0513_preview,
            model_gpt4o
        ]

def get_model_default_openai() -> str:
    return model_gpt3_5_turbo_instruct

def get_model_tools_openai() -> str:
    return model_gpt4o

