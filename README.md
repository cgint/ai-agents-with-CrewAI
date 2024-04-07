
# Based on work from 'Ingmar Stapel'
https://github.com/custom-build-robots/ai-agents-with-CrewAI

# Adaptations I did
Adaptations and some first tryouts using Crew.ai, LangChain, LangSmith, ...

I also use it as a playground to try out function-calling with LangChain.
Additionally testing different LLM-"Runtimes" like OpenAI, Ollama-locally, Together.ai, Groq, Openrouter mostly for function-calling-capablities as the rest works fine usually.

## Function Calling So far:
- OpenAI "gpt-4" did very well
  - "gpt-4-0125-preview" and "gpt-3.5-turbo-instruct" did not work well - lots of syntax-errors on tool-calling
- 'openhermes' on Ollama performed on par with GPT-4
- Mistral, Mixtral, llama2, codellama and even nexusraven had lots of issues with tool-calling running on Ollama
- Experimental [OllamaFunctions](https://python.langchain.com/docs/integrations/chat/ollama_functions/) did not work for me at all
  - Did not invest much time though - just wrapped the OllamaChat and tried out with Mistral, openhermes, Mixtral, ... Nothing worked. Even openhermes that did well without that wrapper :shrug:

### General learnings regarding function calling
- Adding the type of the tool input-parameter (e.g. `def dd_search(query: str):`) lead to less 'irritations' in json returned by the LLM when it comes to name of input-param and also json-format
  - I did not do extensive testing on this though. So it can very well just be the usual small-change/large-effect when prompting LLMs.
### General function calling issues seen throughout all models and providers
```
Action 'DuckDuckGoSearch(query: 'Tesla Company financial performance')' don't exist, these are the only available Actions: SearchTheInternet: SearchTheInternet(query: 'string') - Useful to search the internet about a a given topic and return relevant results
```

I would think that this could be addressed by Crew.ai to 'allow' that ? Alhough I understand that starting to implement special cases will actually lead no where in the long run.

Also I am not sure how much the type-declaration `query: 'string'` is misleading models to think the format is requested like that :shrug:. Further tests show that adding the type actually made things clearer and i saw less 'irritation' e.g. on the parameter-name. When not give names like 'topic' were found in the json returned by the LLM to search the internet although 'query' would be the param-name.

A quick test using `llama2-70b-4096 on Groq` changed the way the tool-call was attempted but still the wrong way - pure string instead of dict.


### Together.ai
Tests using `mistralai/Mixtral-8x7B-Instruct-v0.1` works fine. 

Just some issue like this - did repeat for some time - i guess until 'max value for interations' reached - but the whole crew did finish.

```
Action: None
Action Input: {} 

Action 'None' don't exist, these are the only available Actions: SearchTheInternet: SearchTheInternet(query: 'string') - Useful to search the internet about a a given topic and return relevant results
DuckDuckGoSearch: DuckDuckGoSearch(query: 'string') - Search the web for information on a given topic
```

### Groq
Tests using `mixtral-8x7b-32768` works fine.

Just some of issue issues - but the whole crew did finish. Sometimes lead to hitting rate-limit due to rethinking on these errors I would imaging.
```
Action: Analyze Information
Action Input: {'information': '3M Company recognized as Top 100 Global Innovator 2023, Clarivate has named 3M a Top 100 Global Innovator for 12 consecutive years, 3M Co\'s brand is synonymous with innovation and reliability, a reputation built over a century of operation.'}
 

Action 'Analyze Information' don't exist, these are the only available Actions: SearchTheInternet: SearchTheInternet(query: 'string') - Useful to search the internet about a a given topic and return relevant results
DuckDuckGoSearch: DuckDuckGoSearch(query: 'string') - Search the web for information on a given topic
Delegate work to co-worker: Delegate work to co-worker(coworker: str, task: str, context: str) - Delegate a specific task to one of the following co-workers: [Business Angel and venture capital consultant, Tech content autor]
The input to this tool should be the coworker, the task you want them to do, and ALL necessary context to exectue the task, they know nothing about the task, so share absolute everything you know, don't reference things but instead explain them.
Ask question to co-worker: Ask question to co-worker(coworker: str, question: str, context: str) - Ask a specific question to one of the following co-workers: [Business Angel and venture capital consultant, Tech content autor]
The input to this tool should be the coworker, the question you have for them, and ALL necessary context to ask the question properly, they know nothing about the question, so share absolute everything you know, don't reference things but instead explain them.

Action '** DuckDuckGoSearch(query: 'Tesla Company analysis')
**' don't exist, these are the only available Actions: SearchTheInternet: SearchTheInternet(query: 'string')
```

Tests using `gemma-7b-it` works ... BUT not a single function call is done :wink:

Tests using `llama2-70b-4096` hitting rate-limit due to calling lots of unavailable actions. A lot of delegation action-requests were not available
```
Action 'Delegate work to co-worker(coworker: 'Business Angel and venture capital consultant', task: 'Analyze Tesla Company's financial performance and provide a detailed report', context: 'Please provide a detailed analysis of Tesla Company's financial performance, including revenue, net income, market capitalization, and any other relevant financial metrics. Additionally, please provide an assessment of the company's leadership and management team, their strategy, and their ability to execute on their vision.')' don't exist

Action 'DuckDuckGoSearch(query: 'Tesla Company financial performance')' don't exist, these are the only available Actions: SearchTheInternet: SearchTheInternet(query: 'string') - Useful to search the internet about a a given topic and return relevant results
```

### Openrouter.ai
Tests with `teknium/OpenHermes-2-Mistral-7B`, `anthropic/claude-3-haiku`, `anthropic/claude-3-haiku:beta`, `anthropic/claude-3-sonnet`, `anthropic/claude-3-opus` worked flawless.

Tests using `mistralai/mixtral-8x7b-instruct:nitro` works fine.

Just some of these:
```
Action: Analyze Data

Action Input: 
{'links': ['https://www.wsj.com/market-data/quotes/TSLA/financials/annual/income-statement', 'https://www.wsj.com/market-data/quotes/TSLA/financials', 'https://www.sec.gov/Archives/edgar/data/1318605/000162828023034847/tsla-20230930.htm', 'https://finance.yahoo.com/quote/TSLA/financials/']}

 

Action 'Analyze Data' don't exist, these are the only available Actions: SearchTheInternet: SearchTheInternet(query: 'string') - Useful to search the internet about a a given topic and return relevant results
DuckDuckGoSearch: DuckDuckGoSearch(query: 'string') - Search the web for information on a given topic
Delegate work to co-worker: Delegate work to co-worker(coworker: str, task: str, context: str) - Delegate a specific task to one of the following co-workers: [Business Angel and venture capital consultant, Tech content autor]
The input to this tool should be the coworker, the task you want them to do, and ALL necessary context to exectue the task, they know nothing about the task, so share absolute everything you know, don't reference things but instead explain them.
Ask question to co-worker: Ask question to co-worker(coworker: str, question: str, context: str) - Ask a specific question to one of the following co-workers: [Business Angel and venture capital consultant, Tech content autor]
The input to this tool should be the coworker, the question you have for them, and ALL necessary context to ask the question properly, they know nothing about the question, so share absolute everything you know, don't reference things but instead explain them.
```

Tests using `mistralai/mixtral-8x7b-instruct` lead to several of these:
```
Action: SearchTheInternet

Action Input: {'query': 'Tesla stock price and trend over the past year'}

Observ
Error parsing Tool-Arguments: tool='SearchTheInternet' tool_input="{'query': 'Tesla stock price and trend over the past year'}\n\nObserv" log="\nThought: Apologies for the mistake. I need to provide the input as a dictionary with keys in quotes. I will correct the input and try again.\n\nAction: SearchTheInternet\n\nAction Input: {'query': 'Tesla stock price and trend over the past year'}\n\nObserv"

Thought: It seems there is an issue with the `SearchTheInternet` action. I will try using the `DuckDuckGoSearch` action instead to find the current stock price and trend of Tesla.

Action: DuckDuckGoSearch

Action Input: {'query': 'Tesla stock price and trend over the past year'}

Observ
Error parsing Tool-Arguments: tool='DuckDuckGoSearch' tool_input="{'query': 'Tesla stock price and trend over the past year'}\n\nObserv" log="\nThought: It seems there is an issue with the `SearchTheInternet` action. I will try using the `DuckDuckGoSearch` action instead to find the current stock price and trend of Tesla.\n\nAction: DuckDuckGoSearch\n\nAction Input: {'query': 'Tesla stock price and trend over the past year'}\n\nObserv"

Thought: It appears that there is an issue with both the `SearchTheInternet` and `DuckDuckGoSearch` actions. I will try to use a different approach by delegating this task to a coworker who might have more experience or access to better tools for this specific task. I will delegate the work to the Business Angel and venture capital consultant, as they might have access to financial databases and resources that can provide the required information.

Action: Delegate work to co-worker

Action Input: {'coworker': 'Business Angel and venture capital consultant', 'task': 'Find the current stock price and trend of Tesla over the past year.', 'context': 'I am analyzing Tesla Inc. (TSLA) for potential investment decisions. I need to know the current stock price and its trend over the past year to better understand the company’s financial situation.'}

Observ
Error parsing Tool-Arguments: tool='Delegate work to co-worker' tool_input="{'coworker': 'Business Angel and venture capital consultant', 'task': 'Find the current stock price and trend of Tesla over the past year.', 'context': 'I am analyzing Tesla Inc. (TSLA) for potential investment decisions. I need to know the current stock price and its trend over the past year to better understand the company’s financial situation.'}\n\nObserv" log="\nThought: It appears that there is an issue with both the `SearchTheInternet` and `DuckDuckGoSearch` actions. I will try to use a different approach by delegating this task to a coworker who might have more experience or access to better tools for this specific task. I will delegate the work to the Business Angel and venture capital consultant, as they might have access to financial databases and resources that can provide the required information.\n\nAction: Delegate work to co-worker\n\nAction Input: {'coworker': 'Business Angel and venture capital consultant', 'task': 'Find the current stock price and trend of Tesla over the past year.', 'context': 'I am analyzing Tesla Inc. (TSLA) for potential investment decisions. I need to know the current stock price and its trend over the past year to better understand the company’s financial situation.'}\n\nObserv"
```

Tests using `mistralai/mistral-7b-instruct:free` lead to several of these:
```
Action: SearchTheInternet
Action Input: {
"query": "Current stock price of Tesla (TSLA)"
}

Observ
Error parsing Tool-Arguments: tool='SearchTheInternet' tool_input='{\n"query": "Current stock price of Tesla (TSLA)"\n}\n\nObserv' log='Action: SearchTheInternet\nAction Input: {\n"query": "Current stock price of Tesla (TSLA)"\n}\n\nObserv'
Thought:
Action: DuckDuckGoSearch
Action Input: {
"query": "Current stock price of Tesla (TSLA)"
}

Observ
Error parsing Tool-Arguments: tool='DuckDuckGoSearch' tool_input='{\n"query": "Current stock price of Tesla (TSLA)"\n}\n\nObserv' log='Thought:\nAction: DuckDuckGoSearch\nAction Input: {\n"query": "Current stock price of Tesla (TSLA)"\n}\n\nObserv'
Thought:
Action: Delegate work to co-worker
Action Input:
Error parsing Tool-Arguments: tool='Delegate work to co-worker' tool_input='' log='Thought:\nAction: Delegate work to co-worker\nAction Input:'
Thought:
Action: Ask question to co-worker
Action Input: {
"coworker": "Business Angel and venture capital consultant",
"question": "What is the current stock price of Tesla (TSLA)?",
"context": "Please provide the current stock price of Tesla (TSLA) and any relevant information about its trend over the past year."
}

Observ
Error parsing Tool-Arguments: tool='Ask question to co-worker' tool_input='{\n"coworker": "Business Angel and venture capital consultant",\n"question": "What is the current stock price of Tesla (TSLA)?",\n"context": "Please provide the current stock price of Tesla (TSLA) and any relevant information about its trend over the past year."\n}\n\nObserv' log='Thought:\nAction: Ask question to co-worker\nAction Input: {\n"coworker": "Business Angel and venture capital consultant",\n"question": "What is the current stock price of Tesla (TSLA)?",\n"context": "Please provide the current stock price of Tesla (TSLA) and any relevant information about its trend over the past year."\n}\n\nObserv'
```


# The rest of the README of from the original repo of 'Ingmar Stapel'

# AT-agents realized with CrewAI
This program uses CrewAI to build a web-app using three agents doing some research stuff in the internet.

## Blog Post
To get some more information about the project just visit my blog: https://ai-box.eu/top-story/llm-agenten-arbeiten-eigenstaendig-mit-crewai-automatisieren/1306/


![CrewAI Web-APP](https://ai-box.eu/wp-content/uploads/2024/03/CrewAI_AI_agent_web_app.jpg)

The video is available here: [https://www.youtube.com/watch?v=qMMvO6gsR4A](https://www.youtube.com/watch?v=qMMvO6gsR4A)

This is my blog: [https://ai-box.eu/category/large-language-models/](https://ai-box.eu/category/large-language-models/)
