from config.ai_config import MAX_RETRIES, TARGET_FILE, ACCEPTANCE_THRESHOLD
from agents.review_agent import review_code
from agents.fix_agent import generate_fix
from agents.evalution_agent import evaluate_fix
from agents.validation_agent import validate_code
from utils.file_utils import read_file, write_file, file_exists
from utils.llm_client import call_llm
from agents.memory_agent import MemoryAgent
from agents.diff_agent import analyze_diff
from utils.language_utils import detect_language
from agents.supervisor_agent import build_graph

memory = MemoryAgent()
PLATEAU_LIMIT = 2
MIN_IMPROVEMENT = 3

def run_agentic_fix(instruction: str):

    if not file_exists(TARGET_FILE):
        return {"status": "error", "message": "Target file not found"}

    current_code = read_file(TARGET_FILE)

    graph = build_graph()

    initial_state = {
        "code": current_code,
        "instruction": instruction,
        "retries": 0,
        "score": 0,
        "plateau_count": 0,
        "last_score": None,
        "validation_failed": False,
        "change_ratio": 0
    }

    result = graph.invoke(initial_state)

    write_file(TARGET_FILE, result["code"])

    return {
        "status": "completed",
        "score": result["score"],
        "retries": result["retries"],
        "change_ratio": result["change_ratio"]
    }