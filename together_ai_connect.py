from langchain_together import Together

def get_llm_together(model_name: str, temperature: float, max_tokens: int):
    return Together(model=model_name, temperature=temperature, max_tokens=max_tokens)

model_openhermes = "teknium/OpenHermes-2-Mistral-7B"
model_mixtral_8x7B = "mistralai/Mixtral-8x7B-v0.1"
model_mixtral_8x7B_instruct = "mistralai/Mixtral-8x7B-Instruct-v0.1"
model_mistral_7B_instruct = "mistralai/Mistral-7B-Instruct-v0.2"

def llm_list_together() -> list[str]:
    return [
        model_openhermes,
        model_mixtral_8x7B_instruct,
        model_mistral_7B_instruct,
    ]

def get_model_default_together() -> str:
    return model_openhermes

