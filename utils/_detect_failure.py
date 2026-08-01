
def _detect_failure(tool_results: List[Dict[str, Any]]) -> bool:
    """Any tool result explicitly flagged as an error.

    We do NOT treat empty content as failure — many tools legitimately return
    empty output (zero-result searches, silent bash commands, void writes) and
    penalizing the model for those would corrupt the bandit posterior.
    """
    for r in tool_results:
        if r.get("is_error"):
            return True
    return False

