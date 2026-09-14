import os

from dotenv import load_dotenv
from groq import Groq

from .prompts import SYSTEM_PROMPT


load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY is missing from .env")


client = Groq(api_key=api_key)

MODEL = "openai/gpt-oss-20b"


def get_response_stream(messages):

    full_messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
            + "\n\nIMPORTANT: Never repeat the user's question as a heading or title. Start directly with the answer."
        }
    ] + messages

    try:

        response = client.chat.completions.create(
            model=MODEL,
            messages=full_messages,
            temperature=0.7,
            max_tokens=2048,
            stream=True
        )

        for chunk in response:

            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

    except Exception as e:

        yield (
            "Sorry, I couldn't process your request right now. "
            "Please try again in a moment."
        )