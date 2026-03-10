import os
from typing import TypedDict, Annotated, List

from dotenv import load_dotenv
#from langchain_openai import ChatOpenAI
#from langchain_anthropic import ChatAnthropic
from langchain_ollama import ChatOllama

from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, ToolMessage
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages

from tools import (
    list_available_apartments,
    get_apartment_details,
    search_apartments,
    calculate_total_rent,
    list_all_tenants,
    get_user_preferences,
    create_reservation,
    list_occupied_apartments,
    list_apartments_by_city,
)

load_dotenv()

llm = ChatOllama(model="llama3.2")

tools = [
    list_available_apartments,
    get_apartment_details,
    search_apartments,
    calculate_total_rent,
    list_all_tenants,
    get_user_preferences,
    create_reservation,
    list_occupied_apartments,
    list_apartments_by_city,
]

tools_by_name = {tool.name: tool for tool in tools}

llm_with_tools = llm.bind_tools(tools)


class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]


def assistant_node(state: AgentState):
    system = SystemMessage(content="""
Tu es un assistant immobilier fiable.
Règles :
- Utilise les outils quand la question demande une donnée réelle.
- N'invente jamais un appartement.
- Si une information manque, dis-le clairement.
- Réponds en français.
- Sois clair et professionnel.
""")
    response = llm_with_tools.invoke([system] + state["messages"])
    return {"messages": [response]}


def tools_node(state: AgentState):
    last_message = state["messages"][-1]
    tool_messages = []

    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        for tool_call in last_message.tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]

            tool = tools_by_name[tool_name]
            result = tool.invoke(tool_args)

            tool_messages.append(
                ToolMessage(
                    content=str(result),
                    tool_call_id=tool_call["id"]
                )
            )

    return {"messages": tool_messages}


def router(state: AgentState):
    last_message = state["messages"][-1]
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"
    return END


graph_builder = StateGraph(AgentState)

graph_builder.add_node("assistant", assistant_node)
graph_builder.add_node("tools", tools_node)

graph_builder.set_entry_point("assistant")
graph_builder.add_conditional_edges("assistant", router, {"tools": "tools", END: END})
graph_builder.add_edge("tools", "assistant")

graph = graph_builder.compile()