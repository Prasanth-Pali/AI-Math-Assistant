
from fastapi import FastAPI, HTTPException

app = FastAPI(
    title="AI Math Assistant",
    description="A REST API for mathematical operations",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "Welcome to AI Math Assistant!"
    }


@app.get("/calculate")
def calculate(a: float, b: float, operation: str):
    if operation == "add":
        result = a + b

    elif operation == "subtract":
        result = a - b

    elif operation == "multiply":
        result = a * b

    elif operation == "divide":
        if b == 0:
            raise HTTPException(
                status_code=400,
                detail="Cannot divide by zero"
            )
        result = a / b

    else:
        raise HTTPException(
            status_code=400,
            detail="Unsupported operation"
        )

    return {
        "a": a,
        "b": b,
        "operation": operation,
        "result": result
    }
