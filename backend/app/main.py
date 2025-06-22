from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import openai
import requests
import os
import time
from dotenv import load_dotenv  # ✅ Import dotenv

load_dotenv()  # ✅ Load variables from .env file

openai.api_key = os.getenv("OPENAI_API_KEY")
GITHUB_PAT = os.getenv("GITHUB_PAT")
GITHUB_USER = os.getenv("GITHUB_USER")

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

# Example tool definition
def get_last_commits(repo_name: str, count: int = 3):
    headers = {"Authorization": f"token {GITHUB_PAT}"}
    url = f"https://api.github.com/repos/{GITHUB_USER}/{repo_name}/commits"
    response = requests.get(url, headers=headers, params={"per_page": count})
    data = response.json()
    return [
        {
            "date": c["commit"]["committer"]["date"],
            "sha": c["sha"][:7],
            "message": c["commit"]["message"]
        }
        for c in data
    ]

@app.post("/chat")
async def chat(req: ChatRequest):
    # Thread management
    if req.thread_id:
        thread_id = req.thread_id
    else:
        thread = openai.beta.threads.create()
        thread_id = thread.id

    # Add user message
    openai.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=req.message
    )

    # Run assistant
    run = openai.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=os.getenv("OPENAI_ASSISTANT_ID")
    )

    # Poll until run completes
    while True:
        status = openai.beta.threads.runs.retrieve(thread_id, run.id)
        if status.status == "completed":
            break
        time.sleep(1)

    messages = openai.beta.threads.messages.list(thread_id)
    last_message = messages.data[0].content[0].text.value

    return {"response": last_message, "thread_id": thread_id}
