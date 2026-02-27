# agents/supervisor_agent.py
from typing import Dict, List

class SupervisorAgent:
    def plan(self, state: Dict) -> Dict:
        """
        Decide which agents to execute based on current system state.
        """

        retries = state["retries"]
        max_retries = state["max_retries"]
        score = state["score"]
        threshold = state["threshold"]
        validation_failed = state["validation_failed"]
        plateau_count = state["plateau_count"]
        change_ratio = state["change_ratio"]

        # Stop if max retries reached
        if retries >= max_retries:
            return {
                "action": "stop",
                "reason": "Maximum retries reached",
                "agents_to_run": []
            }

        # Accept if score is sufficient
        if score >= threshold:
            return {
                "action": "accept",
                "reason": "Score meets threshold",
                "agents_to_run": []
            }

        # If validation failed → retry fix only
        if validation_failed:
            return {
                "action": "continue",
                "reason": "Validation failed, retry fix",
                "agents_to_run": ["fix", "validate", "evaluate"]
            }

        # If excessive rewrite → minimal fix
        if change_ratio > 80:
            return {
                "action": "continue",
                "reason": "Excessive rewrite detected",
                "agents_to_run": ["fix", "validate", "evaluate"]
            }

        # If stagnation detected
        if plateau_count >= 2:
            return {
                "action": "stop",
                "reason": "Improvement stagnation detected",
                "agents_to_run": []
            }

        # Default: full pipeline
        return {
            "action": "continue",
            "reason": "Score below threshold",
            "agents_to_run": ["review", "fix", "validate", "evaluate"]
        }