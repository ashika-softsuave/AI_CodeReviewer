from openai import OpenAI
import os
from dotenv import load_dotenv
from config.ai_config import MODEL_NAME

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def call_llm(system_prompt: str, user_prompt: str):

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0
    )

    text_output = response.choices[0].message.content.strip()

    usage = response.usage

    token_info = {
        "input_tokens": usage.prompt_tokens,
        "output_tokens": usage.completion_tokens,
        "total_tokens": usage.total_tokens,
    }

    return text_output, token_info
