from pyexpat import model
from langchain.agents import create_agent
from langchain_community.agent_toolkits.load_tools import load_tools
from langchain_core.tools import Tool
# from langchain_community.llms import Ollama
from langchain_ollama import OllamaLLM
from langchain_openai import ChatOpenAI
from agent.tools.tool_demo4 import calculater

llm = ChatOpenAI(
    model="qwen-max",
    # base_url="http://192.168.31.34:11434",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key="sk-f6e505504e9247ac9593d8a6d22727b8"
)

def get_weather(city: str) -> str:
    """Get the weather for a city."""
    return f"The weather in {city} is sunny."

get_weather_tool = Tool(name="get_weather", func=get_weather,description="")
graph = create_agent(llm, tools=[get_weather_tool, calcculater], system_prompt="You are a helpful assistant.")
graph.invoke()
