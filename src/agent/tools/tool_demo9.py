from typing import Annotated

from agent.my_state import MyState
from langchain_core.messages import ToolMessage
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import tool, InjectedToolCallId
from langgraph.prebuilt import InjectedState
from langgraph.types import Command
from pydantic import BaseModel, Field


# class CalculateArgs(BaseModel):
#     a: float = Field(description="First number")
#     b: float = Field(description="Second number")
#     operation: str = Field(description="Operation to perform, one of (add, subtract, multiply, divide)")

@tool(name_or_callable="greet_user", description="获取当前用户的username之后，生成祝福语句",)
def greet_user(state: Annotated[MyState, InjectedState]) -> str:
   username = state["username"]
   return f"{username}，祝你生日快乐！"

print(greet_user.name)
print(greet_user.description)
print(greet_user.args)
print(greet_user.args_schema.model_json_schema())