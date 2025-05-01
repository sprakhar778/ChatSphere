from langgraph.prebuilt import ToolNode,tools_condition
from langchain.chat_models import init_chat_model
from langchain_community.tools import DuckDuckGoSearchRun,DuckDuckGoSearchResults
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper

from langchain_tavily import TavilySearch
from state import State
from dotenv import load_dotenv
load_dotenv()

# tool =  DuckDuckGoSearchResults(output_format="list")
tavily_search=TavilySearch(max_result=1,topic="news")

wrapper = DuckDuckGoSearchAPIWrapper(region="in-en", source="news")
duck_duck_go_search = DuckDuckGoSearchResults(api_wrapper=wrapper, output_format="list", max_results=3,description="A wrapper around Duck Duck Go Search. Useful for when you need to answer questions about current events. Input should be a search query.")

tools=[duck_duck_go_search]

llm = init_chat_model("meta-llama/llama-4-scout-17b-16e-instruct", model_provider="groq",streaming=True)
llm_with_tool =llm.bind_tools(tools)



MAX_MESSAGES = 5
def trim_messages(messages, max_messages=MAX_MESSAGES):
    return messages[-max_messages:] if len(messages) > max_messages else messages

# Chatbot logic
def chatbot(state: State):
    messages = trim_messages(state["messages"])
    for m in messages:
        m.pretty_print()
    return {"messages": [llm_with_tool.invoke(messages)]}



tool_node=ToolNode(tools=tools)