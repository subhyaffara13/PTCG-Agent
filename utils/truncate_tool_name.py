
def truncate_tool_name(name: str) -> str:
    """
    Truncate tool names that exceed OpenAI's 64-character limit.

    Uses format: {55-char-prefix}_{8-char-hash} to avoid collisions
    when multiple tools have similar long names.

    Args:
        name: The original tool name

    Returns:
        The original name if <= 64 chars, otherwise truncated with hash
    """
    if len(name) <= OPENAI_MAX_TOOL_NAME_LENGTH:
        return name

    # Create deterministic hash from full name to avoid collisions
    name_hash = hashlib.sha256(name.encode()).hexdigest()[:TOOL_NAME_HASH_LENGTH]
    return f"{name[:TOOL_NAME_PREFIX_LENGTH]}_{name_hash}"

