import os
from dotenv import load_dotenv

load_dotenv(override=True)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

MODEL_NAME = "gpt-4o-mini"  # or "gpt-4.1-mini", "gpt-4o"
TEMPERATURE = 0.3