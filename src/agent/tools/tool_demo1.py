from langchain_core.tools import tool
from pydantic import BaseModel, Field


class CalculateArgs(BaseModel):
    a: float = Field(description="First number")
    b: float = Field(description="Second number")
    operation: str = Field(description="Operation to perform, one of (add, subtract, multiply, divide)")

@tool(name_or_callable="calculate", description="Calculate the result of an operation on two numbers.Such as 1 add/subtrace/multiply/divide 2.",
      args_schema=CalculateArgs)
def calculate(a: float, b: float, operation: str) -> float:
    """Calculate the result of an operation on two numbers.Such as 1 add/subtrace/multiply/divide 2."""
    print(f"调用calculate工具: {a} {operation} {b}")
    result = 0.0;
    match operation:
        case "add", "+":
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

print(calculate.name)
print(calculate.description)
print(calculate.args)
print(calculate.args_schema.model_json_schema())