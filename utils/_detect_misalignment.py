from typing import Optional

def _detect_misalignment(prev_user: Optional[str], curr_user: Optional[str]) -> bool:
    """Fires when consecutive user messages share *some* topic (jaccard > 0)
    but are sufficiently different (jaccard < threshold) — i.e. user is
    rephrasing, not changing topic, not repeating."""
    if not prev_user or not curr_user:
        return False
    j = _jaccard(_tokens(prev_user), _tokens(curr_user))
    return 0.0 < j < MISALIGNMENT_JACCARD_THRESHOLD

