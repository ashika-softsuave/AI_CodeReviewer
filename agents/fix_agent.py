from typing import Dict,Tuple
from utils.llm_client import call_llm

SYSTEM_PROMPT = """

You are a precise code transformation agent.

Rules (strict priority order):

1. Follow the instruction exactly.
2. Modify ONLY the parts of code directly relevant to the instruction.
3. Do NOT rewrite or restructure unrelated parts.
4. Preserve overall structure unless the instruction explicitly requires structural change.
5. Do NOT introduce new functionality beyond the instruction.
6. Output must be syntactically valid.
7. If no changes are required, return the original code unchanged.

Return ONLY the updated code.
"""

def generate_fix(code: str, instruction: str, review: str) -> Tuple[str,Dict]:
    prompt = f"""  
Instruction:
{instruction}

Review Findings:
{review}

Code:
{code}

Return updated code only.
"""
    response,tokens = call_llm(SYSTEM_PROMPT, prompt)

    print(f"\n\nFix_agent : {response}")

    return response,tokens
