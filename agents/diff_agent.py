import difflib
from typing import Tuple

def analyze_diff(original_code: str, modified_code: str) -> Tuple[float, dict]:
    """
    Analyze percentage of lines changed between original and modified code.
    Returns:
        change_ratio (0–100)
        detailed stats
    """

    original_lines = original_code.splitlines()
    modified_lines = modified_code.splitlines()

    diff = list(difflib.unified_diff(original_lines, modified_lines))

    changed_lines = 0

    for line in diff:
        if line.startswith("+") and not line.startswith("+++"):
            changed_lines += 1
        elif line.startswith("-") and not line.startswith("---"):
            changed_lines += 1

    total_lines = max(len(original_lines), 1)

    change_ratio = (changed_lines / total_lines) * 100

    stats = {
        "total_lines": total_lines,
        "changed_lines": changed_lines,
        "change_ratio_percent": round(change_ratio, 2)
    }

    return round(change_ratio, 2), stats
