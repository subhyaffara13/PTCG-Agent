
def _get_token_count(details: dict) -> int:
    raw_token_count = details.get("tokenCount", details.get("token_count", 0))
    return raw_token_count if isinstance(raw_token_count, int) else 0

