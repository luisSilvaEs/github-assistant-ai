import os
import time
import openai
from dotenv import load_dotenv
from app.github_tools import get_last_commits

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
ASSISTANT_ID = os.getenv("OPENAI_ASSISTANT_ID")

def ensure_thread(thread_id: str | None) -> str:
    if thread_id:
        print(f"🔹 Reusing thread: {thread_id}", flush=True)
        return thread_id
    thread = openai.beta.threads.create()
    print(f"🔹 Created new thread: {thread.id}", flush=True)
    return thread.id

def send_message_and_get_response(message: str, thread_id: str) -> str:
    print(f"🔸 Sending user message into thread {thread_id}: {message}", flush=True)
    openai.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=message
    )

    run = openai.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=ASSISTANT_ID
    )
    print(f"🔸 Started run: {run.id}", flush=True)

    # poll loop
    while True:
        status = openai.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run.id
        )
        print(f"Run status: {status.status}", flush=True)

        if status.status == "requires_action":
            print("→ requires_action detected", flush=True)
            for tool_call in status.required_action.submit_tool_outputs.tool_calls:
                print(f"→ tool_call: {tool_call.function.name} args={tool_call.function.arguments}", flush=True)
                args = eval(tool_call.function.arguments)

                if tool_call.function.name == "get_last_commits":
                    result = get_last_commits(**args)
                    print(f"→ tool result: {result}", flush=True)

                    openai.beta.threads.runs.submit_tool_outputs(
                        thread_id=thread_id,
                        run_id=run.id,
                        tool_outputs=[{
                            "tool_call_id": tool_call.id,
                            "output": str(result)
                        }]
                    )
                    print("→ submitted tool outputs", flush=True)

            # after handling tool calls, go back to polling
            time.sleep(1)
            continue

        if status.status == "completed":
            print("✅ Run completed", flush=True)
            break

        # in case status is "queued" or "in_progress"
        time.sleep(1)

    messages = openai.beta.threads.messages.list(thread_id)
    final = messages.data[0].content[0].text.value
    print(f"🔹 Final assistant message: {final}", flush=True)
    return final
