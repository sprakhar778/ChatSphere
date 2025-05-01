from langgraph.graph import StateGraph, END
from langgraph.prebuilt import tools_condition
from state import State
from node import (chatbot,tool_node)
from langgraph.checkpoint.memory import MemorySaver

memory = MemorySaver()

graph=StateGraph(State)


graph.add_node("chatbot",chatbot)
graph.add_node("tools",tool_node)

graph.set_entry_point("chatbot")
graph.add_conditional_edges("chatbot", tools_condition, ["tools", END])
graph.add_edge("tools","chatbot")

workflow=graph.compile(checkpointer=memory)

