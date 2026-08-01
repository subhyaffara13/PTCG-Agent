
def _match_bid_to_legal(
    bid: str,
    legal_action_strings: Sequence[str],
) -> str | None:
    """Match a bid (raw integer string) to one of the legal action strings."""
    if bid is None:
        return None
    try:
        bid_int = int(str(bid).strip())
    except ValueError:
        return None
    for legal in legal_action_strings:
        if _bid_from_action_string(legal) == bid_int:
            return legal
    return None

