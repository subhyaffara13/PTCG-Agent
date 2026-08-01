
def _bid_from_action_string(action_string: str) -> int | None:
    """Extract the integer bid from an action string like ``[P0]Bid: 5``."""
    m = _BID_PREFIX_RE.search(action_string)
    if m:
        return int(m.group(1))
    try:
        return int(action_string.strip())
    except ValueError:
        return None

