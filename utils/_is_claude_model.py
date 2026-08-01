
def _is_claude_model(model: str) -> bool:
    """Return True if model name (after stripping snowflake/ prefix) is a Claude model."""
    name = model.lower().removeprefix("snowflake/")
    return any(name.startswith(p) for p in _CLAUDE_MODEL_PREFIXES)

