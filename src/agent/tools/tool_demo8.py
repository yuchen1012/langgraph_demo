from typing import Annotated

from langchain_core.messages import ToolMessage
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import tool, InjectedToolCallId
from langgraph.types import Command
from pydantic import BaseModel, Field


# class CalculateArgs(BaseModel):
#     a: float = Field(description="First number")
#     b: float = Field(description="Second number")
#     operation: str = Field(description="Operation to perform, one of (add, subtract, multiply, divide)")

@tool(name_or_callable="getUserName", description="获取当前用户的username，用来生成祝福语句",)
def get_username(tool_call_id: Annotated[str, InjectedToolCallId],config: RunnableConfig) -> Command:
   username = config['configurable'].get('username', 'zhangzhen')
   return Command(update={
       "username": username, #更新State的username
       # 更新一条工具执行后的消息
       "messages": [
           ToolMessage(content='get username from config', tool_call_id=tool_call_id)
       ]
   })

print(get_username.name)
print(get_username.description)
print(get_username.args)
print(get_username.args_schema.model_json_schema())