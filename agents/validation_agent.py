from typing import Tuple, Dict
from utils.llm_client import call_llm

SYSTEM_PROMPT = """
You are a strict syntax validator.

Tasks:
- Determine if the code is syntactically valid for the specified language
- Do NOT attempt to fix anything
- Do NOT explain

Return format:
VALID
or
INVALID: <short reason>
"""

def validate_code(code: str, language_hint: str)-> Tuple[bool, str, Dict]:

    prompt = f"""
Language:
{language_hint}

Code:
{code}
"""
    result,tokens = call_llm(SYSTEM_PROMPT, prompt)

    if result.startswith("VALID"):
        return True, "OK", tokens

    if result.startswith("INVALID"):
        return False, result, tokens

    return False, "Validator produced unexpected response", tokens
