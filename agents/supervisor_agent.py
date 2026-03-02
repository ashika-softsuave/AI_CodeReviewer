from typing import TypedDict, Optional
from langgraph.graph import StateGraph, END

from agents.review_agent import review_code
from agents.fix_agent import generate_fix
from agents.validation_agent import validate_code
from agents.evalution_agent import evaluate_fix
from agents.diff_agent import analyze_diff
from utils.language_utils import detect_language
from config.ai_config import MAX_RETRIES, ACCEPTANCE_THRESHOLD

# Shared State Definition
class AgentState(TypedDict, total=False):
    code: str
    instruction: str
    retries: int
    score: float
    plateau_count: int
    last_score: Optional[float]
    validation_failed: bool
    change_ratio: float
    next: str
    review: str

# Supervisor Node
def supervisor_node(state: AgentState):

    if state["retries"] >= MAX_RETRIES:
        state["next"] = "end"
        return state

    if state["score"] >= ACCEPTANCE_THRESHOLD:
        state["next"] = "end"
        return state

    if state["plateau_count"] >= 2:
        state["next"] = "end"
        return state

    if state["validation_failed"]:
        state["next"] = "fix"
        return state

    state["next"] = "review"
    return state

# Review Node
def review_node(state: AgentState):
    review, _ = review_code(state["code"], state["instruction"], "")
    state["review"] = review
    return state

# Fix Node
def fix_node(state: AgentState):
    modified_code, _ = generate_fix(
        state["code"], state["instruction"], state.get("review", "")
    )

    change_ratio, _ = analyze_diff(state["code"], modified_code)

    state["code"] = modified_code
    state["change_ratio"] = change_ratio
    return state

# Validation Node
def validate_node(state: AgentState):
    language, _ = detect_language(state["code"])
    valid, _, _ = validate_code(state["code"], language)

    state["validation_failed"] = not valid
    return state

# Evaluation Node
def evaluate_node(state: AgentState):
    if state["validation_failed"]:
        return state

    score, _ = evaluate_fix(state["code"], state["instruction"])

    if state["last_score"] is not None:
        if score - state["last_score"] < 3:
            state["plateau_count"] += 1
        else:
            state["plateau_count"] = 0

    state["last_score"] = score
    state["score"] = score
    state["retries"] += 1

    return state

# Build Graph
def build_graph():

    builder = StateGraph(AgentState)

    # Add Nodes
    builder.add_node("supervisor", supervisor_node)
    builder.add_node("review", review_node)
    builder.add_node("fix", fix_node)
    builder.add_node("validate", validate_node)
    builder.add_node("evaluate", evaluate_node)

    # Entry
    builder.set_entry_point("supervisor")

    # Edges
    builder.add_edge("review", "fix")
    builder.add_edge("fix", "validate")
    builder.add_edge("validate", "evaluate")
    builder.add_edge("evaluate", "supervisor")

    # Conditional routing from supervisor
    builder.add_conditional_edges(
        "supervisor",
        lambda state: state["next"],
        {
            "review": "review",
            "fix": "fix",
            "end": END
        }
    )

    return builder.compile()
