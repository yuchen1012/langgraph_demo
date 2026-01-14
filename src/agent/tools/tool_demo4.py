from langchain_core.tools import tool, StructuredTool
from pydantic import BaseModel, Field


def calculate4(a: float, b: float, operation: str) -> float:
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


async def calculate5(a: float, b: float, operation: str) -> float:
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

calculater = StructuredTool.from_function(
    func=calculate4,
    name="calculate4",
    description="Calculate the result of an operation on two numbers.Such as 1 add/subtrace/multiply/divide 2.",
    return_direct=False,
    coroutine=calculate5
)

print(calculater.name)
print(calculater.description)
print(calculater.args)
print(calculater.args_schema.model_json_schema())