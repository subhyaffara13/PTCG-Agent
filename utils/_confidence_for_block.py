
def _confidence_for_block(
    tag: str,
    block_all: bool,
    tag_in_blocked_list: bool,
) -> float:
    """Return confidence in [0, 1] for this code block detection."""
    normalized = _normalize_language(tag)
    if tag_in_blocked_list:
        return 1.0
    if block_all:
        # Explicit non-executable tags (e.g. text, plaintext) get lower confidence
        if normalized in NON_EXECUTABLE_TAGS:
            return 0.5
        # Untagged or other tags in block-all mode: treat as executable, high confidence
        return 1.0
    return 0.0

