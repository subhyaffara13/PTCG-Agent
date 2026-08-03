from typing import Optional

def _detect_stagnation(prev_asst: Optional[str], curr_asst: Optional[str]) -> bool:
    """Fires when consecutive assistant messages are near-duplicates."""
    if not prev_asst or not curr_asst:
        return False
    j = _jaccard(_tokens(prev_asst), _tokens(curr_asst))
    return j >= STAGNATION_JACCARD_NEAR_DUP

