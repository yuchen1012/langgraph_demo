import asyncio
import json
from typing import Dict, Any, List

from langchain_core.messages import ToolMessage, AIMessage, ToolCall
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.checkpoint.memory import MemorySaver
from langgraph.constants import START, END
from langgraph.graph import MessagesState, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.types import interrupt, Command

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


class BasicToolNode:
    """异步工具节点，用于并发执行AIMessages中请求的工具调用
        功能：
        1、接受工具列表并建立名称索引
        2、并发执行消息中的工具调用请求
        3、自动处理同步|异步工具适配
    """

    def __init__(self, tools: list):
        """
        初始化工具节点
        Args:
            tools: 工具列表
        """
        self.tool_index = {tool.name: tool for tool in tools}  # 所有工具名字的集合

    async def __call__(self, state: Dict[str, Any]) -> Dict[str, List[ToolMessage]]:
        """
        执行工具调用
        Args:
            state: 状态字典, 包含messages键，值为AIMessages对象
        Returns:
            状态字典
        Raises:
            Exception: 如果工具调用失败
        """
        if not (messages := state.get('messages')):
            raise ValueError("No messages found in state")
        message: AIMessage = messages[-1]

        tool_name = message.tool_calls[0]["name"] if message.tool_calls else None
        if tool_name == 'get-station-code-of-citys' or tool_name == 'get-current-date':
            response = interrupt(
                f"AI大模型尝试调用工具 {tool_name}，请审核并选择：批准(y)或直接给我工具执行的答案。"
            )
            # response: 由人工输入的：批准或者拒绝的理由

            if response["answer"] == 'y':
                pass
            else:
                return {"messages": [ToolMessage(
                    content=f"人工终止了工具的调用，给出的理由是{response['answer']}",
                    name = tool_name,
                    tool_call_id = message.tool_calls[0]['id']
                )]}

        output = await self._execute_tool_calls(message.tool_calls)
        return {"messages": output}

    async def _execute_tool_calls(self, tool_calls: List[Dict]) -> List[ToolMessage]:


        async def _invoke_tool(tool_call: Dict) -> ToolMessage:
            try:
                tool = self.tool_index.get(tool_call['name'])
                if not tool:
                    raise KeyError(f"Tool {tool_call['name']} not found")

                if hasattr(tool, 'ainvoke'):
                    tool_result = await tool.ainvoke(tool_call["args"])
                else:
                    loop = asyncio.get_running_loop()
                    tool_result = await loop.run_in_executor(None, tool.invoke, tool_call["args"])

                return ToolMessage(
                    content=json.dumps(tool_result, ensure_ascii=False),
                    name=tool_call['name'],
                    tool_call_id=tool_call['id']
                )
            except Exception as e:

                raise RuntimeError(f"Error invoking tool {tool_call['name']}: {str(e)}")

        try:
            # asyncio.gather() 是Python异步编程中用于并发调度多个协程的核心函数，其核心行为包括；
            # 1. 并发执行；所有传入的协程会被同时调度到时间循环中，通过非阻塞I/O实现并行处理
            # 2. 结果收集；所有协程执行完毕后，其结果（或异常）会以列表的形式返回，与任务完成的顺序无关
            # 3. 异常处理：默认情况下，任意一个任务失败会立即取消其他任务并抛出异常，若设置return_exceptions=True，则异常也作为结果返回
            return await asyncio.gather(*[_invoke_tool(tool_call) for tool_call in tool_calls])
        except Exception as e:
            print(f"并发执行工具时发生错误: {str(e)}")
            raise RuntimeError(f"并发执行工具时发生错误") from e

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
    graph = builder.compile(checkpointer=memory)
    return graph

# graph = asyncio.run(create_graph())
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

    async def execute_graph(user_input: str) -> str:
        result = ''
        current_state = graph.get_state(config)
        if current_state.next:
            human_command = Command(resume={'answer': user_input})
            async for chunk in graph.astream(human_command, config, stream_mode='values'):
                result = prit_message(chunk, result)
            return result
        else:
            async for chunk in graph.astream({'messages': ('user',user_input)}, config, stream_mode='values'):
                result = prit_message(chunk, result)
                if chunk.get("__interrupt__", None):
                   print()

        current_state = graph.get_state(config)
        if current_state.next:
            result = current_state.interrupts[0].value
        return result

    while True:
        user_input = input("User: ")
        res = await execute_graph(user_input)
        print("AI:", res)

if __name__ == '__main__':
    asyncio.run(run_graph())
