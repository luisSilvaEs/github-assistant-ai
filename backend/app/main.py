from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from openai_client import ensure_thread, send_message_and_get_response

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    thread_id: str | None = None

@app.post("/chat")
async def chat(req: ChatRequest):
    thread_id = ensure_thread(req.thread_id)
    response = send_message_and_get_response(req.message, thread_id)
    return {"response": response, "thread_id": thread_id}
