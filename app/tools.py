
import httpx
from langchain.tools import tool


@tool
def calculate(a: float, b: float, operation: str) -> dict:
    """
    Perform a mathematical operation using the AI Math Assistant API.

    Args:
        a: The first number.
        b: The second number.
        operation: One of add, subtract, multiply, or divide.
    """
    allowed_operations = {"add", "subtract", "multiply", "divide"}

    if operation not in allowed_operations:
        raise ValueError(
            f"Unsupported operation: {operation}"
        )

    response = httpx.get(
        "http://127.0.0.1:8000/calculate",
        params={
            "a": a,
            "b": b,
            "operation": operation
        },
        timeout=10.0
    )

    response.raise_for_status()
    return response.json()
