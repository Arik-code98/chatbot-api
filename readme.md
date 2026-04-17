# LLM Chat API

A RESTful API built with FastAPI that enables multi-session, context-aware conversations powered by LLaMA 3.3 70B via the Groq API. Each session maintains its own conversation history, allowing independent, stateful chat interactions through simple HTTP endpoints.

---

## Tech Stack

- **FastAPI** - Web framework for building the API
- **Groq API** - LLM inference backend
- **LLaMA 3.3 70B Versatile** - The underlying large language model
- **Pydantic** - Request body validation
- **python-dotenv** - Environment variable management

---



---

## Setup and Installation

**1. Clone the repository**

```bash
git clone https://github.com/Arik-code98/chatbot-api.git
cd chatbot-api
```

**2. Install dependencies**

```bash
pip install -r requirements.txt
```

**3. Configure environment variables**

Create a `.env` file in the root directory:

```
GROQ_API_KEY=your_groq_api_key_here
```

You can get a free API key from [https://console.groq.com](https://console.groq.com).

**4. Run the server**

```bash
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

---

## API Endpoints

### GET /
Health check to confirm the API is running.

**Response**
```json
{
  "Message": "api is running"
}
```

---

### POST /chats
Send a message within a session. If the session does not exist, it is created automatically. Conversation history is maintained per session, giving the model context across turns.

**Request Body**
```json
{
  "session_id": "user_123",
  "message": "What is machine learning?"
}
```

**Response**

Returns the model's reply as a plain string.

```
"Machine learning is a subset of artificial intelligence..."
```

---

### DELETE /chats/{session_id}
Delete a session and clear its entire conversation history.

**Path Parameter**

| Parameter  | Type   | Description                     |
|------------|--------|---------------------------------|
| session_id | string | The ID of the session to delete |

**Response**
```json
{
  "Message": "Chat deleted",
  "session id": "user_123"
}
```

**Error (404)**
```json
{
  "detail": "chat not found"
}
```

---

## How It Works

1. A client sends a `POST /chats` request with a `session_id` and a `message`.
2. If the session is new, an empty history list is initialized for it.
3. The user's message is appended to the session history as a `user` role message.
4. The full conversation history is sent to the Groq API (LLaMA 3.3 70B).
5. The model's response is appended to the history as an `assistant` role message and returned to the client.
6. On subsequent requests with the same `session_id`, the model receives the full prior context, enabling coherent multi-turn conversation.

---

## Key Concepts Explored

- REST API design with FastAPI
- Multi-session state management using in-memory storage
- Role-based prompt structuring (`user` / `assistant` messages)
- Conversation memory and context passing to an LLM
- Secure API key handling with environment variables
- HTTP exception handling and proper status codes

---

## Notes

- Session data is stored **in memory**. All sessions will be lost if the server restarts. For production use, consider persisting sessions in a database such as Redis or PostgreSQL.
- There is currently no authentication on the endpoints. For production deployments, add API key or JWT-based authentication.
- The model used is `llama-3.3-70b-versatile`. This can be changed to any model supported by the Groq API.
