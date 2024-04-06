import requests
from langchain_core.language_models import BaseLanguageModel
from langchain_community.llms.ollama import Ollama

ollama_ip_address = "127.0.0.1"
ollama_port = "11434"
# ollama_ip_address = "192.168.0.99"
# ollama_port = "11430" # ollama proxy
json_url = "http://" + ollama_ip_address + ":" + ollama_port + "/api/tags"
local_base_url = "http://" + ollama_ip_address + ":" + ollama_port

def get_llm_ollama(model_name: str, temperature: float = 0.1, max_tokens: int = 1000) -> BaseLanguageModel:
    return Ollama(model=model_name, base_url=local_base_url, 
                  num_predict=max_tokens, temperature=temperature, 
                  timeout=90)

def get_models_ollama():
    response = requests.get(json_url)
    if response.status_code == 200:
        data = response.json()
        model_names = [model["name"] for model in data["models"]]
    return model_names

def get_model_default_ollama() -> str:
    # return "openhermes:latest"
    # return "llama2:latest"
    return "mistral:latest"
