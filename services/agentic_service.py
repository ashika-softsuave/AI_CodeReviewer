from config.ai_config import MAX_RETRIES, TARGET_FILE, ACCEPTANCE_THRESHOLD
from agents.review_agent import review_code
from agents.fix_agent import generate_fix
from agents.evalution_agent import evaluate_fix
from agents.decision_agent import decide
from agents.validation_agent import validate_code
from utils.file_utils import read_file, write_file, file_exists
from utils.llm_client import call_llm
from agents.memory_agent import MemoryAgent
from agents.diff_agent import analyze_diff
from agents.supervisor_agent import SupervisorAgent

LANGUAGE_DETECT_PROMPT = """
Detect the programming language of the following code.
Return only the language name.
"""

def detect_language(code: str):
    response, tokens = call_llm(LANGUAGE_DETECT_PROMPT, code)
    print(f"\nLanguage : {response}")
    return response, tokens

memory = MemoryAgent()
PLATEAU_LIMIT = 2
MIN_IMPROVEMENT = 3

def run_agentic_fix(instruction: str):

    if not file_exists(TARGET_FILE):
        return {"status": "error", "message": "Target file not found"}

    supervisor = SupervisorAgent()

    score = 0
    validation_failed = False
    change_ratio = 0
    plateau_count = 0
    retries = 0
    last_score = None

    total_tokens_used = 0
    tokens_report = {}

    # System loads file content into memory.
    current_code = read_file(TARGET_FILE)

    history = memory.load("history", "None")

    while True:

        state = {
            "retries": retries,
            "max_retries": MAX_RETRIES,
            "score": score,
            "threshold": ACCEPTANCE_THRESHOLD,
            "validation_failed": validation_failed,
            "plateau_count": plateau_count,
            "change_ratio": change_ratio
        }

        plan = supervisor.plan(state)

        print("\nSupervisor Plan:", plan)
        if plan["action"] == "stop":
            return {
                "status": "stopped",
                "reason": plan["reason"],
                "score": score,
                "retries": retries,
                "tokens": tokens_report,
                "total_tokens": total_tokens_used
            }

        if plan["action"] == "accept":
            write_file(TARGET_FILE, current_code)
            return {
                "status": "success",
                "reason": plan["reason"],
                "score": score,
                "retries": retries,
                "tokens": tokens_report,
                "total_tokens": total_tokens_used
            }

        agents_to_run = plan["agents_to_run"]
        iteration_tokens = 0

        # Dynamic Agent Execution
        if "review" in agents_to_run:
            review, token1 = review_code(current_code, instruction, history)
            iteration_tokens += token1["total_tokens"]
        else:
            review = None

        if "fix" in agents_to_run:
            modified_code, token2 = generate_fix(current_code, instruction, review)
            iteration_tokens += token2["total_tokens"]

            change_ratio, diff_stats = analyze_diff(current_code, modified_code)
            current_code = modified_code

        if "validate" in agents_to_run:
            language, token3 = detect_language(current_code)
            iteration_tokens += token3["total_tokens"]

            valid, message, token4 = validate_code(current_code, language)
            iteration_tokens += token4["total_tokens"]

            validation_failed = not valid

        if "evaluate" in agents_to_run and not validation_failed:
            val_score, token5 = evaluate_fix(current_code, instruction)
            iteration_tokens += token5["total_tokens"]

            score = val_score

            if last_score is not None:
                if score - last_score < 3:
                    plateau_count += 1
                else:
                    plateau_count = 0

            last_score = score

        tokens_report[f"iteration{retries + 1}"] = iteration_tokens
        total_tokens_used += iteration_tokens

        retries += 1
