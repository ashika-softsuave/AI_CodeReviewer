from utils.llm_client import call_llm

LANGUAGE_DETECT_PROMPT = """
Detect the programming language of the following code.
Return only the language name.
"""

def detect_language(code: str):
    response, tokens = call_llm(LANGUAGE_DETECT_PROMPT, code)
    print(f"\nLanguage : {response}")
    return response, tokens