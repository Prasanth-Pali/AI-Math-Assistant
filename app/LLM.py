
import os
from dotenv import load_dotenv
from langchain.messages import HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field

# Load environment variables from .env
load_dotenv()

# Read Gemini API key
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("GOOGLE_API_KEY not found in .env file")

# Initialize Gemini LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-3.8-flash",
    google_api_key=api_key,
    temperature=0
)

messages = [
    SystemMessage(
        content="You are a helpful AI math assistant. "
                "Explain concepts in simple English."
    ),
    HumanMessage(
        content="What is the difference between an LLM and an AI agent?"
    )
]

#Pydantic Model
class AIResponse(BaseModel):

    # Contains the detailed answer to the user's question.
    answer: str = Field(
        description="Answer to the user's question"
    )

    # Contains a short summary of the answer.
    summary: str = Field(
        description="Summary of the answer"
    )

structured_llm = llm.with_structured_output(AIResponse)

# Send a message to the LLM
response = structured_llm.invoke(messages)

# Print the LLM response
print(response.answer)
