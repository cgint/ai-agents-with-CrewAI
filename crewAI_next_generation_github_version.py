# Adaptations and some first tryouts using Crew.ai, LangChain, LangSmith
# Also a playground to try out function-calling with LangChain and also
# different LLM-"Runtimes" like OpenAI, Ollama-locally, Together.ai.
#
# Funciton Calling So far:
#   Ollama-Openhermes performed on par with GPT-4
#   Ollama and Mistral, Mixtral, llama2, codellama and even nexusraven had lots of issues

# Based on work from
# https://github.com/custom-build-robots/ai-agents-with-CrewAI
# Autor:    Ingmar Stapel
# Datum:    20240330
# Version:  1.0
# Homepage: https://ai-box.eu/

import asyncio

# Create a new event loop
loop = asyncio.new_event_loop()

# Set the event loop as the current event loop
asyncio.set_event_loop(loop)

import time
from uuid import uuid4
from crewai import Agent, Task, Crew
from crewai_tools import tool
from langsmith import RunTree, traceable
import streamlit as st
from langchain.prompts import PromptTemplate
from langchain.chains.llm import LLMChain


# Source
# The following GitHub repo helped me alot to build this app
# URL: https://github.com/joaomdmoura/crewAI

# This video hleped me to get the streamlit agent callback functionality running
# URL: https://www.youtube.com/watch?v=nKG_kbQUDDE

# The repository from Tony Kipkemboi explains very nice how to use agents and tools.
# The SearchTools is from his repository.
#https://github.com/tonykipkemboi/trip_planner_agent

from model_helper import get_llm, get_model_defaults, get_models
from tasks import get_task_desc_autor, get_task_desc_business_angel, get_task_desc_researcher

# my_question="What about investing in 3M Company (stock ticker symbol 'MMM') ?"
# my_question="What about investing in 3M Company (MMM) ?"
# my_question="What about investing in 3M Company ?"
# my_question="What about investing in Tesla Company (stock ticker symbol 'TSLA') ?"
my_question="What can technology startups contribute to make the world a better place?"
import model_helper

model_helper.use_provider = "gemini" # available providers: "openai", "openrouter", "together", "ollama", "groq", "gemini"

model_default, model_tools = get_model_defaults()
model_names = None
model_names = get_models()
model_default_id=model_names.index(model_default)
model_tools_id=model_names.index(model_tools)

if model_names is None:
    st.error("Failed to fetch data via 'get_models'.")

st.set_page_config(page_title="Your network of AI agents")

tab0, tab4, tab1, tab3, tab2 = st.tabs(["Main: ", "The tasks", "Researcher: ", "Business Angel: ", "Autor: "])

task_value_1 = "empty"
task_value_2 = "empty"
task_value_3 = "empty"

# This is more or less a work around that hopefully will work for the dd_search.
@tool("SearchTheInternet")
@traceable
def search_search(query: str):
    """Useful to search the internet about a a given topic and return relevant results"""
    s = rt.create_child(
        name="SearchTheInternet",
        run_type="tool",
        inputs={"query": query}
    )
    from tools.search_tools import SearchTools
    search_result: str = SearchTools.search_internet(query)
    s.end(outputs={'search_result': search_result})
    s.post()
    return search_result

# This is more or less a work around that hopefully will work for the dd_search.
@tool('DuckDuckGoSearch')
@traceable
def dd_search(query: str):
    """Search the web for information on a given topic"""
    # Install duckduckgo-search for this example:
    # !pip install -U duckduckgo-search
    from langchain_community.tools.ddg_search import DuckDuckGoSearchRun
    s = rt.create_child(
        name="DuckDuckGoSearch",
        run_type="tool",
        inputs={"query": query}
    )
    search_result: str = DuckDuckGoSearchRun().run(query)
    s.end(outputs={'search_result': search_result})
    s.post()
    return search_result

# To display what the agents are currently doing this streamlit_callback function is needed.
def streamlit_callback(step_output):
    # This function will be called after each step of the agent's execution
    st.markdown("---")
    for step in step_output:
        if isinstance(step, tuple) and len(step) == 2:
            action, observation = step
            if isinstance(action, dict) and "tool" in action and "tool_input" in action and "log" in action:
                st.markdown(f"# Action")
                st.markdown(f"**Tool:** {action['tool']}")
                st.markdown(f"**Tool Input** {action['tool_input']}")
                st.markdown(f"**Log:** {action['log']}")
                st.markdown(f"**Action:** {action['Action']}")
                st.markdown(
                    f"**Action Input:** ```json\n{action['tool_input']}\n```")
            elif isinstance(action, str):
                st.markdown(f"**Action:** {action}")
            else:
                st.markdown(f"**Action:** {str(action)}")

            st.markdown(f"**Observation**")
            if isinstance(observation, str):
                observation_lines = observation.split('\n')
                for line in observation_lines:
                    if line.startswith('Title: '):
                        st.markdown(f"**Title:** {line[7:]}")
                    elif line.startswith('Link: '):
                        st.markdown(f"**Link:** {line[6:]}")
                    elif line.startswith('Snippet: '):
                        st.markdown(f"**Snippet:** {line[9:]}")
                    elif line.startswith('-'):
                        st.markdown(line)
                    else:
                        st.markdown(line)
            else:
                st.markdown(str(observation))
        else:
            st.markdown(step)

# Now set the session state for the text variables.
if "text_task_in1" not in st.session_state:
    st.session_state.text_task_in1 = None

if "text_task_in2" not in st.session_state:
    st.session_state.text_task_in2 = None

if "text_task_in3" not in st.session_state:
    st.session_state.text_task_in3 = None


with tab1:
  st.subheader("Your research agent:")

  # Populate the dropdown box
  model_researcher = st.selectbox('Select a LLM model for the researcher:', model_names, key="model_researcher", index=model_tools_id)

  # Create a slider to select the temperature of the llm
  temperature_researcher = st.slider('Select a LLM temperature value between 0 and 1 [higher is more creative, lower is more coherent]', key="temperature_researcher", min_value=0.0, max_value=1.0, step=0.01)

  max_iterations_researcher = st.selectbox('Set the max value for interations:', ('1', '2', '5', '10', '15', '20', '25'), key="iter_researcher", index=1)
  ollama_llm_researcher = get_llm(model_researcher, temperature_researcher)

  role_researcher = st.text_area('role:','Senior research analyst', key="role_researcher", height=20)
  goal_researcher = st.text_area('goal:', 'As a Senior Research Analyst, you play a key role in analyzing data to offer strategic insights for decision-making. This requires strong analytical skills, critical thinking, and industry knowledge.', key="goal_researcher", height=200)
  backstory_researcher = st.text_area('backstory:', 'As a Senior Research Analyst, you hold an advanced degree in fields like economics or statistics. With expertise in research methodologies and data analysis, you execute projects across diverse industries. Your insights aid decision-making, and you stay updated on industry trends through continuous learning.', key="backstory_researcher", height=200)

with tab2:
  st.subheader("Your author agent:")

  model_autor = st.selectbox('Select a LLM model for the autor:', model_names, key="model_autor", index=model_default_id)

  # Create a slider to select the temperature of the llm
  temperature_autor = st.slider('Select a LLM temperature value between 0 and 1 [higher is more creative, lower is more coherent]', key="temperature_autor", min_value=0.0, max_value=1.0, step=0.01)

  max_iterations_autor = st.selectbox('Set the max value for interations:', ('1', '2', '5', '10', '15', '20', '25'), key="iter_autor", index=1)
  ollama_llm_autor = get_llm(model_autor, temperature_autor)


  role_autor = st.text_area('role:','Tech content autor', key="role_autor", height=20)
  goal_autor = st.text_area('goal:', 'As a Tech Content Author you are playing a crucial role in creating and curating high-quality content focused on technology topics. This role requires a combination of technical expertise, writing proficiency, and the ability to communicate complex concepts in a clear and engaging manner.', 
                            key="goal_autor", height=200)
  backstory_autor = st.text_area('backstory:', 'As a Tech Content Author, you hold a degree in journalism, communications, computer science, or related fields. With a passion for technology, you possess a deep understanding of technical concepts and trends. Starting your career in roles like technical writing or content creation, you have honed strong writing skills and the ability to simplify complex ideas. Through continuous learning, you stay updated on emerging technologies, ensuring your content remains relevant in the ever-changing tech landscape.', 
                                 key="backstory_autor", height=200)


with tab3:
  # This is the tab which is used to define the agent specifig llm agent.
  # All the description below is used as an example that the user of that web-app
  # has an idea how to define such an agent.
  st.subheader("Your investor agent:")

  model_consultant = st.selectbox('Select a LLM model for the agent:', model_names, key="model_consultant", index=model_tools_id)
  # Create a slider to select the temperature of the llm
  temperature_consultant = st.slider('Select a LLM temperature value between 0 and 1 [higher is more creative, lower is more coherent]', key="temperature_consultant", min_value=0.0, max_value=1.0, step=0.01)

  # Set the max value how long an agent is allowed to interate.
  max_iterations_consultant = st.selectbox('Set the max value for interations:', ('1', '2', '5', '10', '15', '20', '25'), key="iter_consultant", index=1)
  
  # Define the llm call for the ollama server we like to use for our agent  
  ollama_llm_consultant = get_llm(model_consultant, temperature_consultant)

  # Define now our agent
  role_consultant = st.text_area('role:','Business Angel and venture capital consultant', key="role_consultant", height=20)
  goal_consultant = st.text_area('goal:', 'As a Business Angels and Venture Capital Consultant you are playing a vital role in the startup ecosystem by providing funding, mentorship, and strategic guidance to early-stage companies. While their roles share similarities, they differ in terms of investment focus, funding sources, and level of involvement.', 
                key="goal_consultant", height=200)
  backstory_consultant = st.text_area('backstory:', 'Business Angels and Venture Capital Consultants typically possess extensive experience in finance, entrepreneurship, and investment management. They may have backgrounds in fields such as investment banking, private equity, corporate finance, or startup leadership. Many have built successful careers in the financial industry, gaining expertise in deal sourcing, due diligence, portfolio management, and strategic advisory.', 
                                      key="backstory_consultant", height=200)

with tab4:
  st.subheader("The agent tasks:")

  st.session_state.text_task_in1 = st.text_area('Task 1 Researcher:', get_task_desc_researcher(), key="text_task_in_1")
  st.session_state.text_task_in2 = st.text_area('Task 2 Autor / Writer:', get_task_desc_autor(), key="text_task_in_2")
  st.session_state.text_task_in3 = st.text_area('Task 3 Business Angel:', get_task_desc_business_angel(), key="text_task_in_3")

  task_in_1_new = st.session_state.text_task_in1 if "text_task_in1" in st.session_state else None
  task_in_2_new = st.session_state.text_task_in2 if "text_task_in2" in st.session_state else None
  task_in_3_new = st.session_state.text_task_in3 if "text_task_in3" in st.session_state else None 

with tab0:
  st.title('Do my analysis')
  st.text(f'Using provider: "{model_helper.use_provider}"')
  task_description = st.text_area('Your short task description here is used to re-write Task 1 - Task 3 so that they fit thematically with the new input.', value=my_question)

  model_rewrite = st.selectbox('Select a LLM model for re-writing the tasks 1 - 3:', model_names, key="model_rewrite", index=model_default_id)

  # Create a slider to select the temperature of the llm
  temperature_rewrite_task = st.slider('Select a LLM temperature value between 0 and 1 [higher is more creative, lower is more coherent]', min_value=0.0, max_value=1.0, step=0.01)

  if st.button('Start Generation NOW'):
    run_id = uuid4()
    start_time = time.time()
    rt: RunTree = RunTree(
        session_name="ai-agents-with-CrewAI",
        name="Start Generation NOW",
        inputs={"model_default": model_default, "model_tools": model_tools, "task_description": task_description},
        id=run_id
    )
    rewrite_task = rt.create_child(
        name="Rewrite Tasks",
        inputs={"model_rewrite": model_rewrite, "temperature_rewrite_task": temperature_rewrite_task, "task_description": task_description}
    )
    with st.status("🤖 **Now rewriting the tasks for your three agents...**", state="running", expanded=True) as status:
          ollama_llm_rewrite_task = get_llm(model_rewrite, temperature_rewrite_task)

          template_task_1 = "As an AI assistant please write a task description for an AI agent whos role is to be a researcher who like to understand various topics. This is an example task description for an AI agent. The AI agent needs this task to understand what he has to do. \n Example task description:\n" + st.session_state.text_task_in1 + "\n Please rewrite this task description for the new topic which is described as follows: \n New topic: \n{task_description} \nImportant for the rewritten new task description is to keep the structure of the example task description provided."
          prompt_task_1 = PromptTemplate(template=template_task_1, input_variables=["task_description"])
          llm_chain = LLMChain(prompt=prompt_task_1, llm=ollama_llm_rewrite_task)
          task_in_1_new_cr: str = llm_chain.run({"task_description": task_description})

          template_task_3 = "As an AI assistant please write a task description for an AI agent whos role is an business angle investor who does analysis. This is an example task description for an AI agent. The AI agent needs this task to understand what he has to do. \n Example task description:\n" + st.session_state.text_task_in3 + "\n Please rewrite this task description for the new topic which is described as follows: \n New topic: \n{task_description} \nImportant for the rewritten new task description is to keep the structure of the example task description provided."
          prompt_task_3 = PromptTemplate(template=template_task_3, input_variables=["task_description"])
          llm_chain = LLMChain(prompt=prompt_task_3, llm=ollama_llm_rewrite_task)
          task_in_3_new: str = llm_chain.run({"task_description": task_description})

          template_task_2 = "As an AI assistant please write a task description for an AI agent whos role is to be an autor who likes to write articles. This is an example task description for an AI agent. The AI agent needs this task to understand what he has to do. \n Example task description:\n" + st.session_state.text_task_in2 + "\n Please rewrite this task description for the new topic which is described as follows: \n New topic: \n{task_description} \nImportant for the rewritten new task description is to keep the structure of the example task description provided."
          prompt_task_2 = PromptTemplate(template=template_task_2, input_variables=["task_description"])
          llm_chain = LLMChain(prompt=prompt_task_2, llm=ollama_llm_rewrite_task)
          task_in_2_new: str = llm_chain.run({"task_description": task_description})

          st.text_area('Task 1 Researcher rewritten:', task_in_1_new.strip(), key="text_task_in_1_re")
          st.text_area('Task 3 Business Angel rewritten:', task_in_3_new.strip(), key="text_task_in_3_re")
          st.text_area('Task 2 Autor / Writer rewritten:', task_in_2_new.strip(), key="text_task_in_2_re")

    rewrite_task.end(outputs={'task_in_1_new': task_in_1_new, 'task_in_2_new': task_in_2_new, 'task_in_3_new': task_in_3_new})
    rewrite_task.post()

    # Define your agents with roles and goals
    researcher = Agent(
      max_inter=max_iterations_researcher,
      role=role_researcher,
      goal=goal_researcher,
      backstory=backstory_researcher,

      verbose=True,
      allow_delegation=True,
      tools=[
         search_search,
          dd_search,
      ],
      llm=ollama_llm_researcher, 
      step_callback=streamlit_callback
    )

    consultant = Agent(
      max_inter=max_iterations_consultant,
      role=role_consultant,
      goal=goal_consultant,
      backstory=backstory_consultant,

      verbose=True,
      allow_delegation=False,
      tools=[
          search_search,
          dd_search,
      ],
      llm=ollama_llm_consultant, 
      step_callback=streamlit_callback
    )

    autor = Agent(
      max_inter=max_iterations_autor,
      role=role_autor ,
      goal=goal_autor,
      backstory=backstory_autor,
      verbose=True,
      allow_delegation=False,
      llm=ollama_llm_autor,
      step_callback=streamlit_callback
    )

    # Create tasks for your agents
    task1 = Task(
      description=task_in_1_new,
      agent=researcher,
      expected_output="Do my work please"
    )

    # Create tasks for your agents
    task2 = Task(
      description=task_in_2_new,
      agent=autor,
      expected_output="Do my work please"
    )

    # Create tasks for your agents
    task3 = Task(
      description=task_in_3_new,
      agent=consultant,
      expected_output="Do my work please"
    )
    rt_work: RunTree = rt.create_child(
        name="Doing work",
        inputs={"model_researcher": model_researcher, "model_consultant": model_consultant, "model_autor": model_autor}
    )
    with st.status("🤖 **Agents doing your work...**", state="running", expanded=True) as status:
        with st.container(height=800, border=False):
          crew = Crew(
            agents=[researcher, consultant, autor],
            tasks=[task1, task3, task2],
            verbose=2, # You can set it to 1 or 2 to different logging levels
            # memory=True # uses OpenAI Embeddings by default - can be configured - see https://docs.crewai.com/core-concepts/Memory/#example-configuring-memory-for-a-crew
          )
          result = crew.kickoff()
        status.update(label="✅ Research activity finished!",
                      state="complete", expanded=False)
    rt_work.end(outputs={'result': result})
    rt_work.post()
    rt.end(outputs={'result': result})
    rt.post()
    end_time = time.time()
    duration_sec = int(end_time - start_time)
    print("######################")
    print(result)
    st.subheader(f'Your requested analysis is ready and took {duration_sec} seconds :sunglasses:')
    st.markdown(result)

    st.download_button(
        label="Download",
        data=result, 
        file_name="meeting_prep.md",
        mime="text/plain"
    )
