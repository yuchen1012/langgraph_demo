import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from agent.my_llm import llm
from langgraph.prebuilt import create_react_agent

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

mcp_client = MultiServerMCPClient({
    'python_mcp': python_mcp_server_config,
    'java_mcp': java_mcp_server_config
})


async def create_agent():
    """必须是异步的"""
    mcp_tools = await mcp_client.get_tools()
    print(mcp_tools)
    mcp_prompt1 = await mcp_client.get_prompt(server_name='python_mcp', prompt_name='ask_about_topic',
                                              arguments={'topic': '深度学习'})
    print(mcp_prompt1)
    mcp_resources = await mcp_client.get_resources(server_name='python_mcp', uris='resource://config')
    print(mcp_resources[0])
    print(mcp_resources[0].data)

    return create_react_agent(
        llm,
        tools=mcp_tools,
        prompt="你是一个智能助手，尽可能调用工具来回答用户的问题",
    )


agent = asyncio.run(create_agent())
