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


def chat(
    messages,
    system=None,
    stop_sequences=None,
):
    params = {
        "model": model,
        "max_tokens": 4000,
        "messages": messages,
        "stop_sequences": stop_sequences or [],
    }

    if system:
        params["system"] = [
            {
                "type": "text",
                "text": system,
                "cache_control": {"type": "ephemeral"},
            }
        ]

    message = client.messages.create(**params)
    return message


def text_from_message(message):
    return "\n".join([block.text for block in message.content if block.type == "text"])


# Prompt with ~6k Tokens
code_prompt = (Path(__file__).parent.parent / "prompts" / "code_prompt.md").read_text(
    encoding="utf-8"
)


if __name__ == "__main__":
    messages = []

    add_user_message(messages, "what's 1+1")

    print(chat(messages, system=code_prompt))
