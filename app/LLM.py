
import os

from dotenv import load_dotenv
from langchain.messages import HumanMessage, SystemMessage
from langchain_groq import ChatGroq
from pydantic import BaseModel, Field

from app.tools import calculate


# 1. Load environment variables
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GOOGLE_API_KEY not found in .env file")


# 2. Initialize Gemini LLM
llm = ChatGroq(
    model="openai/gpt-oss-20b",
    api_key=api_key,
    temperature=0
)


# 3. Define the structured response
class AIResponse(BaseModel):
    answer: str = Field(
        description="Detailed answer to the user's question"
    )

    summary: str = Field(
        description="Short summary of the answer"
    )


# 4. Create conversation messages
messages = [
    SystemMessage(
        content=(
            "You are a helpful AI math assistant. "
            "Use the available tool for mathematical calculations. "
            "After receiving the tool result, explain the answer "
            "in simple English. Return both answer and summary."
        )
    ),
    HumanMessage(
         content="What is 10 multiplied by 20? Use the calculation tool."
    )
]


# 5. Bind the tool to Gemini
llm_with_tools = llm.bind_tools(
    [calculate],
    tool_choice="calculate"
)

# 6. Ask Gemini to choose and call the tool
tool_call_response = llm_with_tools.invoke(messages)

print("Tool calls:", tool_call_response.tool_calls)


# 7. Execute the requested tool
if not tool_call_response.tool_calls:
    raise RuntimeError("Gemini did not request a tool call.")

tool_results = []

for tool_call in tool_call_response.tool_calls:
    if tool_call["name"] == calculate.name:
        result = calculate.invoke(tool_call["args"])
        print("Actual API result:", result)
        tool_results.append({
            "name": tool_call["name"],
            "result": result
        })
    else:
        raise ValueError(
            f"Unknown tool requested: {tool_call['name']}"
        )


# 8. Prepare the tool result for the final LLM call
final_messages = messages + [
    tool_call_response,
    HumanMessage(
        content=(
            "Tool execution result: "
            f"{tool_results}. "
            "Use this result to provide the final answer."
        )
    )
]


# 9. Generate a Pydantic structured response
structured_llm = llm.with_structured_output(AIResponse)

response = structured_llm.invoke(final_messages)


# 10. Print the final response
print("\nFinal Answer:")
print(response.answer)

print("\nSummary:")
print(response.summary)

print("\nResponse type:", type(response).__name__)
