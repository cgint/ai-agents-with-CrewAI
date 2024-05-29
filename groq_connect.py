from langchain_groq import ChatGroq

def get_llm_groq(model_name: str, temperature: float, max_tokens: int):
    return ChatGroq(model_name=model_name, temperature=temperature, max_tokens=max_tokens)

model_llama2_70b = "llama2-70b-4096"
model_llama3_8b = "llama3-8b-8192"
model_llama3_70b = "llama3-70b-8192"
model_mixtral_8x7B_instruct = "mixtral-8x7b-32768"
model_gemma_7B_instruct = "gemma-7b-it"

def get_models_groq() -> list[str]:
    return [
        model_mixtral_8x7B_instruct,
        model_gemma_7B_instruct,
        model_llama2_70b,
        model_llama3_8b,
        model_llama3_70b
    ]

def get_model_default_groq() -> str:
    return model_llama3_8b

def get_model_tools_groq() -> str:
    return model_llama3_70b

