from typing import Annotated
from langchain_core.tools import tool
from pydantic import BaseModel, Field


@tool(name_or_callable='calculate')
def calculate2(a: Annotated[float, 'First number'], b: Annotated[float, 'Second number'],
               operation: Annotated[str, 'Operation to perform, one of (add, subtract, multiply, divide)']) -> float:
    """Calculate the result of an operation on two numbers.Such as 1 add/subtrace/multiply/divide 2."""
    print(f"调用calculate工具: {a} {operation} {b}")
    result = 0.0;
    match operation:
        case "add" | "+":
            result = a + b;
        case "subtrace":
            result = a - b;
        case "multiply":
            result = a * b;
        case "divide":
            if b != 0:
                result = a / b;
            else:
                raise Exception("除数不能为0");
    return result;


print(calculate2.name)
print(calculate2.description)
print(calculate2.args)
print(calculate2.args_schema.model_json_schema())
print(calculate2.invoke({'a': 1, 'b': 2, 'operation': "+"}))
