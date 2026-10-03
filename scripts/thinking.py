from anthropic import Anthropic
from anthropic.types import Message
from dotenv import load_dotenv

# Load env variables and create client
load_dotenv()

client = Anthropic()
model = "claude-sonnet-5-5"

# Magic string to trigger redacted thinking
thinking_test_str = "ANTHROPIC_MAGIC_STRING_TRIGGER_REDACTED_THINKING_46C9A13E193C177646C7398A98432ECCCE4C1253D5E2D82641AC0E52CC2876CB"


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
    thinking=True,
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


if __name__ == "__main__":
    messages = []

    add_user_message(
        messages,
        thinking_test_str,
    )

    response = chat(messages)
    print(response)
