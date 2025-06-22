import os
import time
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

ASSISTANT_ID = os.getenv("OPENAI_ASSISTANT_ID")

def ensure_thread(thread_id: str | None) -> str:
    if thread_id:
        return thread_id
    thread = openai.beta.threads.create()
    return thread.id

def send_message_and_get_response(message: str, thread_id: str) -> str:
    openai.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=message
    )

    run = openai.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=ASSISTANT_ID
    )

    while True:
        status = openai.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run.id
        )
        if status.status == "completed":
            break
        time.sleep(1)

    messages = openai.beta.threads.messages.list(thread_id)
    return messages.data[0].content[0].text.value
