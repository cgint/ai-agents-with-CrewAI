from typing import Optional
from langchain_core.language_models import BaseLanguageModel
from langchain_community.chat_models.openai import ChatOpenAI
import os

class ChatOpenRouter(ChatOpenAI):
    openai_api_base: str
    openai_api_key: str
    model_name: str

    def __init__(self,
                 model_name: str,
                 openai_api_key: Optional[str] = None,
                 openai_api_base: str = "https://openrouter.ai/api/v1",
                 **kwargs):
        openai_api_key = openai_api_key or os.getenv('OPENROUTER_API_KEY')
        super().__init__(openai_api_base=openai_api_base,
                         openai_api_key=openai_api_key,
                         model_name=model_name, **kwargs)
        
def get_llm_openrouter(model_name: str, temperature: float, max_tokens: int) -> BaseLanguageModel:
    return ChatOpenRouter(model_name=model_name, openai_api_key=os.getenv("OPENROUTER_API_KEY"), 
                         temperature=temperature, max_tokens=max_tokens)

model_openhermes = "teknium/OpenHermes-2-Mistral-7B"
model_mixtral_8x7B_instruct = "mistralai/mixtral-8x7b-instruct"
model_mixtral_8x7B_instruct_nitro = "mistralai/mixtral-8x7b-instruct:nitro"
model_mistral_7B_20_instruct = "mistralai/mistral-7b-instruct:nitro"
model_mistral_7b_10_free = "mistralai/mistral-7b-instruct:free"
model_openai_35_turbo_instruct = "openai/gpt-3.5-turbo-instruct"
model_openai_4_turbo_preview = "openai/gpt-4-turbo-preview"
model_anthropic_claude3_haiku = "anthropic/claude-3-haiku"
model_anthropic_claude3_haiku_self_moderated = "anthropic/claude-3-haiku:beta"
model_anthropic_claude3_sonnet = "anthropic/claude-3-sonnet"
model_anthropic_claude3_opus = "anthropic/claude-3-opus"

def llm_list_openrouter() -> list[str]:
    return [
        model_openhermes,
        model_mixtral_8x7B_instruct,
        model_mixtral_8x7B_instruct_nitro,
        model_mistral_7B_20_instruct,
        model_mistral_7b_10_free,
        model_openai_35_turbo_instruct,
        model_openai_4_turbo_preview,
        model_anthropic_claude3_haiku,
        model_anthropic_claude3_haiku_self_moderated,
        model_anthropic_claude3_sonnet,
        model_anthropic_claude3_opus
    ]

def get_model_default_openrouter() -> str:
    return model_mistral_7B_20_instruct

def get_model_tools_openrouter() -> str:
    return model_openhermes

