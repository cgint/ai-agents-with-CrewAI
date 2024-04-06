# Based on work from Ingmar Stapel
https://github.com/custom-build-robots/ai-agents-with-CrewAI

# Adaptations I did
Adaptations and some first tryouts using Crew.ai, LangChain, LangSmith, ...

I also use it as a playground to try out function-calling with LangChain.
Additionally testing different LLM-"Runtimes" like OpenAI, Ollama-locally, Together.ai, Groq, Openrouter mostly for function-calling-capablities as the rest works fine usually.

## Funciton Calling So far:
- Ollama-Openhermes performed on par with GPT-4
- Ollama and Mistral, Mixtral, llama2, codellama and even nexusraven had lots of issues
- Experimental [OllamaFunctions](https://python.langchain.com/docs/integrations/chat/ollama_functions/) did not work for me at all
  - Did not invest much time though - just wrapped the OllamaChat and tried out with Mistral, openhermes, Mixtral, ... Nothing worked. Even openhermes that did well without that wrapper :shrug:


# AT-agents realized with CrewAI
This program uses CrewAI to build a web-app using three agents doing some research stuff in the internet.

## Blog Post
To get some more information about the project just visit my blog: https://ai-box.eu/top-story/llm-agenten-arbeiten-eigenstaendig-mit-crewai-automatisieren/1306/


![CrewAI Web-APP](https://ai-box.eu/wp-content/uploads/2024/03/CrewAI_AI_agent_web_app.jpg)

The video is available here: [https://www.youtube.com/watch?v=qMMvO6gsR4A](https://www.youtube.com/watch?v=qMMvO6gsR4A)

This is my blog: [https://ai-box.eu/category/large-language-models/](https://ai-box.eu/category/large-language-models/)
