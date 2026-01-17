import os
from pyexpat import model

import dotenv
from agent.tools.tool_demo5 import runnale_tool
from agent.tools.tool_demo6 import my_search_tool, MySearchTool
from agent.tools.tool_demo8 import get_username
from agent.tools.tool_demo9 import greet_user
from langchain_core.messages import AnyMessage
from langchain.agents import create_agent, AgentState
from langchain_community.agent_toolkits.load_tools import load_tools
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import Tool
# from langchain_community.llms import Ollama
from langchain_ollama import OllamaLLM
from langchain_openai import ChatOpenAI
from agent.tools.tool_demo3 import calculate
from langgraph.prebuilt import create_react_agent
from agent.my_state import MyState

dotenv.load_dotenv()
llm = ChatOpenAI(
    model="qwen-max",
    # base_url="http://192.168.31.34:11434",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key=os.environ.get("DASH_SCOPE_KEY")
)

def get_weather(city: str) -> str:
    """Get the weather for a city."""
    return f"The weather in {city} is sunny."

get_weather_tool = Tool(name="get_weather", func=get_weather,description="")
my_search_tool = MySearchTool();

#提示词模版的函数: 由用户传入内容，组成一个动态的系统提示词
def prompt(state: AgentState, config: RunnableConfig) -> list[AnyMessage]:
    username = config["configurable"].get("username", "zhangzhen")
    print(username)
    system_msg = f"你是一个智能助手，尽可能的调用工具来回答用户的问题，当前用户的名字是{username}"
    return [{'role':'system', 'content':system_msg}] + state['messages']


graph = create_react_agent(llm, tools=[get_weather_tool, calculate, runnale_tool, my_search_tool, get_username, greet_user], prompt = prompt,
                           state_schema=MyState)
# graph.invoke()
