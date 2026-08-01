
def is_anthropic_oauth_key(value: Optional[str]) -> bool:
    """Check if a value contains an Anthropic OAuth token (sk-ant-oat*)."""
    if value is None:
        return False
    # Handle both raw token and "Bearer <token>" format
    if value.startswith("Bearer "):
        value = value[7:]
    return value.startswith(ANTHROPIC_OAUTH_TOKEN_PREFIX)

