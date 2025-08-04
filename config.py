import os
from dotenv import load_dotenv
from openai import OpenAI
load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY environment variable not set.")

openAiClient = OpenAI(api_key=openai_api_key)