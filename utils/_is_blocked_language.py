
def _is_blocked_language(
    tag: str,
    blocked_languages: Optional[List[str]],
    block_all: bool,
) -> bool:
    """True if this language tag should be considered blocked."""
    normalized = _normalize_language(tag)
    if block_all:
        # Block all: only allow through if it's explicitly non-executable (we still block but with lower confidence)
        return True
    # When block_all is False, caller guarantees blocked_languages is non-empty.
    if not blocked_languages:
        return True
    normalized_list = [_normalize_language(t) for t in blocked_languages]
    return normalized in normalized_list

