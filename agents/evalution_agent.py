from typing import Tuple, Dict
from utils.llm_client import call_llm
import json

SYSTEM_PROMPT = """
You are a strict evaluator.

Evaluate the modified code using these dimensions:

1. Correctness (0-100)
2. Instruction Compliance (0-100)
3. Completeness (0-100)
4. Safety (0-100)

Return JSON only in this format:

{
  "correctness": <number>,
  "compliance": <number>,
  "completeness": <number>,
  "safety": <number>
}
"""

def evaluate_fix(code: str, instruction: str) -> Tuple[int, Dict]:

    prompt = f"""
Instruction:
{instruction}

Code:
{code}
"""

    text, tokens = call_llm(SYSTEM_PROMPT, prompt)

    try:
        scores = json.loads(text)

        weighted_score = (
            scores["correctness"] * 0.35 +
            scores["compliance"] * 0.25 +
            scores["completeness"] * 0.20 +
            scores["safety"] * 0.20
        )

        return int(weighted_score), tokens

    except:
        return 0, tokens