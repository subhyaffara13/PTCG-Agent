
def _compute_overall_action(results: List[GuardrailTestResultEntry]) -> str:
    """Return the worst-case action: blocked > masked > error > unsupported > passed."""
    priority = {"blocked": 4, "masked": 3, "error": 2, "unsupported": 1, "passed": 0}
    worst = "passed"
    for r in results:
        if priority.get(r["action"], 0) > priority.get(worst, 0):
            worst = r["action"]
    return worst

