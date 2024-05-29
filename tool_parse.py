
from crewai.agents.parser import CrewAgentParser
import ast
cap = CrewAgentParser()

input_parse_works = """I need to conduct a comprehensive analysis of the current financial situation and future prospects of Tesla Company (stock ticker symbol 'TSLA').

Action: SearchTheInternet
Action Input: {
  "query": "Tesla financial report"
}"""
input_parse_error = """I need to conduct a comprehensive analysis of the current financial situation and future prospects of Tesla Company (stock ticker symbol 'TSLA').

Action: SearchTheInternet
Action Input: {
    "query": "Tesla financial report"
}

Observation"""
input_parse_error2 = """I need to conduct a comprehensive analysis of the current financial situation and future prospects of Tesla Company (stock ticker symbol 'TSLA').

Action: SearchTheInternet
Action Input: {
    "query": "Tesla financial report"
}
Observation: So"""
input_parse_error3 = """I need to conduct a comprehensive analysis of the current financial situation and future prospects of Tesla Company (stock ticker symbol 'TSLA').

Action: SearchTheInternet
Action Input: {
    "query": "Tesla financial report"
}

Observation: Some observation"""

input_list = [
    input_parse_works,
    input_parse_error,
    input_parse_error2,
    input_parse_error3
]

expected_result = {'query': 'Tesla financial report'}
msgs = []
for i, input in enumerate(input_list):
  try:
    parsed = cap.parse(input)
    res: dict = ast.literal_eval(parsed.tool_input)
    if res != expected_result:
      raise Exception(f"Error parsing input {i}: {res} does not match {expected_result}")
    msgs.append(f"Success parsing input {i}")
  except Exception as e:
    msgs.append(f"Error parsing input {i}: {e}")


print("\n".join(msgs))

