from http.client import responses

from anyio.lowlevel import checkpoint
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.store.postgres import PostgresStore

from agent.my_llm import llm
from agent.tools.tool_demo6 import MySearchTool
from agent.tools.tool_demo8 import get_username
from agent.tools.tool_demo9 import greet_user
from agent.tools.tool_demo3 import calculate
from langgraph.prebuilt import create_react_agent
from agent.my_state import MyState

# checkpoint = InMemorySaver() # 短期记忆在内存中

DB_URI = "postgresql://postgres:password@localhost:5432/mydb"

with (PostgresSaver.from_conn_string(DB_URI) as checkpoint,
      PostgresStore.from_conn_string(DB_URI) as store):
    # checkpoint.setup() #第一次调用
    store.setup() #第一次调用

    my_search_tool = MySearchTool();
    agent = create_react_agent(
        llm,
        tools=[calculate, my_search_tool, get_username, greet_user],
        prompt="你是一个智能助手，尽可能调用工具来回答用户的问题",
        state_schema=MyState,
        checkpointer=checkpoint,
        store=store
    )

    config = {
        "configurable": {
            "thread_id": "2"
        }
    }

    responses1 = agent.invoke({"messages": [{'role': 'user', 'content': '1加1等于多少？'}]}, config)
    print(responses1['messages'][-1].content)

    responses2 = agent.invoke({"messages": [{'role': 'user', 'content': '那加5呢？'}]}, config)

    print(responses2['messages'][-1].content)
    result = list(agent.get_state_history(config))
    print(result)
