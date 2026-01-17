from langchain_core.tools import tool
from pydantic import BaseModel, Field



@tool(name_or_callable="calculate")
def calculate(a: float, b: float, operation: str) -> float:
    """Calculate the result of an operation on two numbers.Such as 1 add/subtrace/multiply/divide 2.

    Args:
        a (float): First number
        b (float): Second number
        operation (str): Operation to perform, one of (add, subtract, multiply, divide)
    Returns:
        float: Result of the operation
    """
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

print(calculate.name)
print(calculate.description)
print(calculate.args)
print(calculate.args_schema.model_json_schema())