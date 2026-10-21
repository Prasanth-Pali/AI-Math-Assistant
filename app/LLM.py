
import os

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

from app.tools import calculate

load_dotenv()

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0,
)


class AIResponse(BaseModel):
    answer: str = Field(description="Detailed answer")
    summary: str = Field(description="Short summary")


agent = create_agent(
    model=llm,
    tools=[calculate],
    system_prompt=(
        "You are a helpful AI math assistant. "
        "Use the calculate tool for mathematical calculations. "
        "Never invent calculation results. "
        "Explain the result in simple English."
    ),
)


question = input("Ask a math question: ")

result = agent.invoke({
    "messages": [
        {"role": "user", "content": question}
    ]
})

answer = result["messages"][-1].content

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "Convert the answer into the required structure. "
        "Do not change the calculation result."
    ),
    ("human", "{answer}"),
])

messages = prompt.format_messages(answer=answer)

structured_llm = llm.with_structured_output(AIResponse)

response = structured_llm.invoke(messages)

print("\n--- Final Answer ---")
print(response.answer)

print("\n--- Summary ---")
print(response.summary)

print("\nResponse type:", type(response).__name__)
