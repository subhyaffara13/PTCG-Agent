import re

def _sanitize_anthropic_tool_use_id(tool_use_id: str) -> str:
    """
    Sanitize tool_use_id to match Anthropic's required pattern: ^[a-zA-Z0-9_-]+$

    Anthropic requires tool_use_id to only contain alphanumeric characters, underscores, and hyphens.
    This function replaces any invalid characters with underscores.
    """
    # Replace any character that's not alphanumeric, underscore, or hyphen with underscore
    sanitized = re.sub(r"[^a-zA-Z0-9_-]", "_", tool_use_id)
    # Ensure it's not empty (fallback to a default if needed)
    if not sanitized:
        sanitized = "tool_use_id"
    return sanitized

