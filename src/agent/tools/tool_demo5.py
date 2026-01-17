from itertools import chain

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from agent.my_llm import llm
from langchain_core.tools import tool
from pydantic import BaseModel, Field


class RunnaleToolArgs(BaseModel):
    topic: str = Field(description="报幕词的主题")
    language: str = Field(description="报幕词的语言")


prompt = (
    PromptTemplate.from_template("生成一个简短，关于{topic}的报幕词。"
                                 + "要求内容简短，采用{language}")
)

chain = prompt | llm | StrOutputParser()

runnale_tool = chain.as_tool(name="chain_tool",
                             description="这是一个专门用于生成报幕词的工具",
                             args_schema=RunnaleToolArgs)

print(runnale_tool)
