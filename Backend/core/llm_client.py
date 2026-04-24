from openai import OpenAI
from config import OPENAI_API_KEY, MODEL_NAME, TEMPERATURE

client = OpenAI(api_key=OPENAI_API_KEY)


def call_llm(prompt: str) -> str:
    """Call OpenAI LLM and return raw text response."""
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": "You generate structured technical proposals in strict JSON format only."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=TEMPERATURE
    )
    return response.choices[0].message.content