import asyncio
import json
from typing import Dict, Any, List

from langchain_core.messages import ToolMessage, AIMessage, ToolCall
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.checkpoint.memory import MemorySaver
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
    builder.add_edge("tools", "chatbot")

    memory = MemorySaver()

    graph = builder.compile(checkpointer=memory, interrupt_before=['tools'])
    return graph


async def run_graph():
    graph = await create_graph()
    config = {
        "configurable": {
            "thread_id": "123213"
        }
    }

    def prit_message(event, result):
        messages = event.get('messages')
        if messages:
            if isinstance(messages, list):
                message = messages[-1]
            if message.__class__.__name__ == 'AIMessage':
                if message.content:
                    print(message.content)
                    result = message.content
            msg_repr = message.pretty_repr(html=True)
            if len(msg_repr) > 1500:
                msg_repr = msg_repr[:1500] + '...(已截断)'
            print(msg_repr)
        return result

    def get_answer(tool_message, user_answer):
        tool_name = tool_message.tool_calls[0]['name']
        answer = (
            f"人工终止了工具：{tool_name}的执行，拒绝的理由是:{user_answer}"
        )

        new_message = [
            ToolMessage(content=answer, tool_call_id = tool_message.tool_calls[0]['id']),
            AIMessage(content=answer)
        ]

        graph.update_state(
            # 手动修改消息
            config = config,
            values={'messages': new_message}
        )


    async def execute_graph(user_input: str) -> str:
        result = ''
        if user_input.strip().lower() != 'y':
            current_state = graph.get_state(config)
            if current_state.next: # 如果有下一步，则表示当前工作流处于中断中
                tools_message = current_state.values['messages'][-1]
                # 通过提供关于请求的更改/改变主意的指示来满足工具调用
                get_answer(tools_message, user_input)
                message = graph.get_state(config).values['messages'][-1]
                result = message.content
                return  result
            else:
                async for chunk in graph.astream({"messages": ('user', user_input)}, config, stream_mode='values'):
                    result = prit_message(chunk, result)
        else:
            async for chunk in graph.astream(None, config, stream_mode='values'):
                result = prit_message(chunk, result)

        current_state = graph.get_state(config)
        if current_state.next:
            ai_message = current_state.values['messages'][-1]
            tool_name = ai_message.tool_calls[0]['name']
            result = f"AI助手即将执行{tool_name}工具，是否批准？输入'y'表示批准，其他输入表示拒绝并说明理由"
        return result

    while True:
        user_input = input("User: ")
        res = await execute_graph(user_input)
        print("AI:", res)

if __name__ == '__main__':
    asyncio.run(run_graph())
