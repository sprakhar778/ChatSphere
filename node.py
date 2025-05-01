from langgraph.prebuilt import ToolNode,tools_condition
from langchain.chat_models import init_chat_model
from langchain_community.tools import DuckDuckGoSearchResults
from langchain_tavily import TavilySearch
from state import State
from dotenv import load_dotenv
load_dotenv()

# tool =  DuckDuckGoSearchResults(output_format="list")
tool=TavilySearch(max_result=1,topic="news")
tools=[tool]

llm = init_chat_model("meta-llama/llama-4-scout-17b-16e-instruct", model_provider="groq",streaming=True)
llm_with_tool =llm.bind_tools(tools)



MAX_MESSAGES = 5
def trim_messages(messages, max_messages=MAX_MESSAGES):
    return messages[-max_messages:] if len(messages) > max_messages else messages

# Chatbot logic
def chatbot(state: State):
    messages = trim_messages(state["messages"])
    print(messages)
    return {"messages": [llm_with_tool.invoke(messages)]}



tool_node=ToolNode(tools=tools)