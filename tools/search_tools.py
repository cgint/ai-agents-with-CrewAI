import json
from langsmith import traceable

import requests
import streamlit as st
from langchain.tools import tool


class SearchTools():

  @tool("SearchTheInternet")
  @traceable
  def search_internet(query):
    """Useful to search the internet
    about a a given topic and return relevant results"""

    top_result_to_return = 4
    url = "https://google.serper.dev/search"
    payload = json.dumps({"q": query})
    headers = {
        'X-API-KEY': st.secrets['SERPER_API_KEY'],
        'content-type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    tool_answer = ""
    # check if there is an organic key
    if 'organic' not in response.json():
      tool_answer = "Sorry, I couldn't find anything about that, there could be an error with you serper api key."
    else:
      results = response.json()['organic']
      string = []
      for result in results[:top_result_to_return]:
        try:
          string.append('\n'.join([
              f"Title: {result['title']}", f"Link: {result['link']}",
              f"Snippet: {result['snippet']}", "\n-----------------"
          ]))
        except KeyError:
          next

      tool_answer = '\n'.join(string)
    return tool_answer
