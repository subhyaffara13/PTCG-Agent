
def _detect_loop(history: List[str], new_calls: List[Dict[str, Any]]) -> bool:
    """Fires if any new call's signature appears >= LOOP_REPEAT_THRESHOLD-1 times
    in recent history (so this call would be the Nth)."""
    if not new_calls:
        return False
    for call in new_calls:
        sig = _signature(call)
        recent_count = history.count(sig)
        if recent_count >= LOOP_REPEAT_THRESHOLD - 1:
            return True
    return False

