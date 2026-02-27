# review agent
from typing import Tuple,Dict

from utils.llm_client import call_llm

SYSTEM_PROMPT = """
You are a senior code reviewer.

Analyze the provided code and produce a technical review.

Evaluation dimensions:
- Correctness and potential failure causes
- Language mismatch or partial conversions
- Code quality and structure
- Maintainability and readability
- Performance concerns
- Security risks and unsafe patterns
- Best practices and conventions

Guidelines:
- Be precise and technical
- Identify concrete problems, not generic advice
- Do not propose full rewrites
- Return ONLY the review
"""

def review_code(code: str, instruction: str, history: str) -> Tuple[str, Dict]:
    prompt = f"""
Instruction:
{instruction}

Previous Issues:
{history}

Code:
{code}
"""
    response,tokens = call_llm(SYSTEM_PROMPT, prompt)

    print(f"\n\n: {response}")

    return response,tokens
