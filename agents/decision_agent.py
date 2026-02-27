from config.ai_config import ACCEPTANCE_THRESHOLD, MAX_RETRIES

def decide(score: float, retries: int, plateau_count: int) -> dict:

    if plateau_count >= 2:
        return {
            "accepted": False,
            "score": score,
            "reason": "Stopped due to stagnation trend",
            "threshold": ACCEPTANCE_THRESHOLD
        }

    if retries >= MAX_RETRIES - 1 and score < ACCEPTANCE_THRESHOLD:
        return {
            "accepted": False,
            "score": score,
            "reason": "Max retries reached without meeting threshold",
            "threshold": ACCEPTANCE_THRESHOLD
        }

    accepted = score >= ACCEPTANCE_THRESHOLD

    if accepted:
        reason = (
            f"Accepted: score {score} meets or exceeds "
            f"threshold {ACCEPTANCE_THRESHOLD}"
        )
    else:
        reason = (
            f"Rejected: score {score} below "
            f"threshold {ACCEPTANCE_THRESHOLD}"
        )

    return {
        "accepted": accepted,
        "score": score,
        "threshold": ACCEPTANCE_THRESHOLD,
        "reason": reason
    }