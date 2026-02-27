#Configuration files
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

MODEL_NAME = "gpt-4o-mini"
MAX_RETRIES = 3

TARGET_FILE = "ashika.python"
ACCEPTANCE_THRESHOLD = 90


