import base64
from pathlib import Path

from anthropic import Anthropic
from anthropic.types import Message
from dotenv import load_dotenv

# Load env variables and create client
load_dotenv()

client = Anthropic()
model = "claude-sonnet-5-5"


def add_user_message(messages, message):
    user_message = {
        "role": "user",
        "content": message.content if isinstance(message, Message) else message,
    }
    messages.append(user_message)


def add_assistant_message(messages, message):
    assistant_message = {
        "role": "assistant",
        "content": message.content if isinstance(message, Message) else message,
    }
    messages.append(assistant_message)


def chat(
    messages,
    system=None,
    stop_sequences=None,
    tools=None,
    thinking=False,
):
    params = {
        "model": model,
        "max_tokens": 4000,
        "messages": messages,
        "stop_sequences": stop_sequences or [],
    }

    if thinking:
        params["thinking"] = {"type": "adaptive", "display": "summarized"}

    if tools:
        params["tools"] = tools

    if system:
        params["system"] = system

    message = client.messages.create(**params)
    return message


def text_from_message(message):
    return "\n".join([block.text for block in message.content if block.type == "text"])


if __name__ == "__main__":
    pdf_path = Path(__file__).parent.parent / "documents" / "earth.pdf"

    with open(pdf_path, "rb") as f:
        file_bytes = base64.standard_b64encode(f.read()).decode("utf-8")

    messages = []

    add_user_message(
        messages,
        [
            {
                "type": "document",
                "source": {
                    "type": "base64",
                    "media_type": "application/pdf",
                    "data": file_bytes,
                },
                "title": "Earth Article",
                "citations": {"enabled": True},
            },
            {
                "type": "text",
                "text": "How were Earth's atmosphere and oceans were formed?",
            },
        ],
    )

    response = chat(messages)

    for block in response.content:
        if block.type == "text" and block.citations:
            for c in block.citations:
                print(f"Page {c.start_page_number}: {c.cited_text.strip()}")
