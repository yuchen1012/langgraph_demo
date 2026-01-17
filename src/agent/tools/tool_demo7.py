# from langchain_core.runnables import RunnableConfig
# from langchain_core.tools import tool
# from pydantic import BaseModel, Field
#
#
# # class CalculateArgs(BaseModel):
# #     a: float = Field(description="First number")
# #     b: float = Field(description="Second number")
# #     operation: str = Field(description="Operation to perform, one of (add, subtract, multiply, divide)")
#
# @tool(name_or_callable="getUserName", description="get username from config",
#       )
# def get_username_by_config(config: RunnableConfig) -> str:
#    username = config['configurable'].get('username', 'zhangzhen')
#    return username
#
# print(calculate.name)
# print(calculate.description)
# print(calculate.args)
# print(calculate.args_schema.model_json_schema())