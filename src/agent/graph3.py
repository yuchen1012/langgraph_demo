import asyncio
import json
from typing import Dict, Any, List

from langchain_core.messages import ToolMessage, AIMessage, ToolCall
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.constants import START, END
from langgraph.graph import MessagesState, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition

from agent.my_llm import llm

python_mcp_server_config = {
    'url': 'http://127.0.0.1:3001/sse',
    'transport': 'sse',
    # 'url':'http://127.0.0.1:3002/streamable',
    # 'transport':'streamable'
}

java_mcp_server_config = {
    'url': 'http://127.0.0.1:8127/sse',
    'transport': 'sse',
}

my12306_mcp_server_config = {
    "url": "https://mcp.api-inference.modelscope.net/461c771c134549/sse",
    "transport": "sse"
}

my_view_mcp_server_config = {
    "url": "https://mcp.api-inference.modelscope.net/34c09a22bb8647/sse",
    "transport": "sse"
}

mcp_client = MultiServerMCPClient({
    'python_mcp': python_mcp_server_config,
    'java_mcp': java_mcp_server_config,
    '12306': my12306_mcp_server_config,
    'view': my_view_mcp_server_config
})

class State(MessagesState):
    pass

async def create_graph():
    tools = await mcp_client.get_tools()

    builder = StateGraph(State)

    async def chatbot(state: State):
        llm_with_tools = llm.bind_tools(tools)
        return {'messages': [await llm_with_tools.ainvoke(state['messages'])]}

    tool_node = ToolNode(tools)

    builder.add_node('chatbot', chatbot)
    builder.add_node('tools', tool_node)

    builder.add_conditional_edges("chatbot", tools_condition)
    builder.add_edge(START, "chatbot")
    builder.add_edge("tools ", "chatbot")
    graph = builder.compile()
    return graph

graph = asyncio.run(create_graph())

