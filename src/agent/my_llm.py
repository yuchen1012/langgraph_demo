import dotenv
from langchain_openai import ChatOpenAI
from os import environ
import os

dotenv.load_dotenv()
llm = ChatOpenAI(
    model="qwen-max",
    # base_url="http://192.168.31.34:11434",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key=os.environ.get("DASH_SCOPE_KEY")
)