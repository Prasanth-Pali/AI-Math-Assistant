# 🧮 AI Math Assistant

An AI-powered mathematical assistant built with **Python, FastAPI, LangChain, and Groq LLM**. The application combines natural language understanding with API-based mathematical calculations to provide accurate, structured responses.

The project demonstrates how to integrate an LLM with existing REST APIs using LangChain tools and agents, rather than relying entirely on the LLM to perform calculations.

## 🚀 Key Features

- **REST API:** Mathematical operations exposed through FastAPI.
- **AI Agent:** Uses LangChain to interpret user questions and decide when to call a tool.
- **LLM Integration:** Uses Groq's `openai/gpt-oss-20b` model.
- **Tool Calling:** Connects the LangChain `calculate` tool to the existing FastAPI calculation endpoint.
- **Structured Responses:** Uses Pydantic to return an answer and a concise summary.
- **Prompt Templates:** Separates LLM instructions from dynamic input using `ChatPromptTemplate`.
- **Input Validation:** Supports defined mathematical operations and handles division by zero.
- **Environment Configuration:** Loads API credentials from environment variables.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Application development |
| FastAPI | REST API development |
| Uvicorn | ASGI server |
| LangChain | Agent orchestration and tool integration |
| Groq | LLM inference |
| Pydantic | Structured response validation |
| HTTPX | HTTP requests from the tool to the API |
| python-dotenv | Environment variable management |
| Pytest | Python testing framework dependency |

## 🏗️ Architecture

```text
User
  |
  v
AI Math Assistant
  |
  v
LangChain Agent <------> Groq LLM
  |
  | Tool call when needed
  v
calculate Tool
  |
  | HTTP GET request
  v
FastAPI /calculate Endpoint
  |
  v
Mathematical Result
  |
  v
Agent Final Answer
  |
  v
ChatPromptTemplate
  |
  v
Pydantic AIResponse
  |
  v
Answer + Summary
```

### How It Works

1. The user enters a mathematical question.
2. The LangChain agent analyzes the question and decides whether to use the `calculate` tool.
3. The tool sends an HTTP request to the existing FastAPI endpoint.
4. FastAPI validates the requested operation and performs the calculation.
5. The agent uses the API result to formulate its final answer.
6. A separate prompt template passes that answer to the LLM for structured formatting.
7. Pydantic validates the response against the `AIResponse` model.

**Note:** The current implementation makes two LLM calls: one for agent execution and another for structured response generation.

## 📁 Project Structure

```text
AI-Math-Assistant/
│
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI application and calculation endpoint
│   ├── tools.py         # LangChain tool calling the REST API
│   └── LLM.py           # Groq integration, agent and structured output
│
├── tests/               # Test directory
│
├── .env                 # Local API credentials (not committed)
├── .gitignore
├── requirements.txt
└── README.md
```

## ⚙️ Getting Started

### Prerequisites

- Python 3.11 or a compatible Python version supported by the installed dependencies
- A Groq API key
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/Prasanth-Pali/AI-Math-Assistant.git
cd AI-Math-Assistant
```

### 2. Create a Virtual Environment

**Windows PowerShell**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```powershell
python -m pip install -r requirements.txt
python -m pip install langchain-groq
```

Ensure `langchain-groq` is also listed in `requirements.txt` so the project dependencies are reproducible.

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
```

Replace the placeholder with your own API key.

**Security:** Never commit `.env` or expose your API key in source code, screenshots, or public repositories.

## ▶️ Running the Application

The project currently runs as two components: the REST API and the AI agent.

### Terminal 1: Start the FastAPI Server

```powershell
python -m uvicorn app.main:app --reload --reload-dir app
```

API base URL:

`http://127.0.0.1:8000`

Interactive API documentation:

`http://127.0.0.1:8000/docs`

Keep this terminal running while using the AI agent.

### Terminal 2: Start the AI Assistant

Activate the virtual environment, navigate to the project root, and run:

```powershell
python -m app.LLM
```

Enter a mathematical question when prompted.

Example:

```text
Ask a math question: What is 25 plus 17?

Answer: 25 plus 17 equals 42.
Summary: 25 + 17 = 42.
```

The exact wording may vary depending on the LLM response.

## 🔌 REST API Reference

### Calculate a Mathematical Operation

**Endpoint:** `GET /calculate`

**Base URL:** `http://127.0.0.1:8000`

| Parameter | Type | Description |
|---|---|---|
| `a` | Float | First operand |
| `b` | Float | Second operand |
| `operation` | String | `add`, `subtract`, `multiply`, or `divide` |

Example request:

```http
GET /calculate?a=10&b=20&operation=multiply
```

Example response:

```json
{
  "a": 10.0,
  "b": 20.0,
  "operation": "multiply",
  "result": 200.0
}
```

Supported operations:

- `add` — Addition
- `subtract` — Subtraction
- `multiply` — Multiplication
- `divide` — Division

Unsupported operations and division by zero are handled as API errors.

## 🧠 Structured Response Model

The application uses Pydantic to define the response structure:

```python
class AIResponse(BaseModel):
    answer: str
    summary: str
```

Example response fields:

```json
{
  "answer": "10 multiplied by 20 equals 200.",
  "summary": "10 × 20 = 200."
}
```

This makes it easier for future application components to consume the answer and summary as separate fields.

## 🧪 Example Questions

Try these questions with the assistant:

- What is 25 plus 17?
- Calculate 144 divided by 12.
- What is 9 multiplied by 8?
- What can you help me with?

Mathematical questions should use the calculation tool when the agent determines that it is needed. General questions may be answered directly by the LLM.

## 🔐 Engineering Considerations

This project demonstrates a separation of responsibilities:

- **FastAPI** owns the calculation logic.
- **LangChain** manages agent execution and tool calls.
- **Groq LLM** interprets natural language and generates responses.
- **Pydantic** validates the structured response.
- **Environment variables** keep credentials outside application source code.

For production deployment, additional work would be needed for automated tests, authentication, rate limiting, API timeouts and retries, structured logging, monitoring, and deployment configuration.

## 🗺️ Future Enhancements

Potential improvements include:

- Integrate the AI assistant with a web UI.
- Add automated tests for the REST API, tool, and agent.
- Add retry handling and more robust API error reporting.
- Introduce conversation history and follow-up questions.
- Add Docker-based deployment and a CI/CD pipeline.
- Explore more advanced agent workflows and observability.

These are planned improvements, not currently implemented features.

## 👨‍💻 Author

**Prasanth Pali**

GitHub: [Prasanth-Pali](https://github.com/Prasanth-Pali)

Project Repository: [AI-Math-Assistant](https://github.com/Prasanth-Pali/AI-Math-Assistant)

---

*Built as a hands-on project to explore LLM integration, LangChain agents, tool calling, REST APIs, and structured AI responses.*
