
def _is_azure_claude_model(model: str) -> bool:
    """
    Check if a model name contains 'claude' (case-insensitive).
    Used to detect Claude models that need Anthropic-specific handling.
    """
    try:
        model_lower = model.lower()
        return "claude" in model_lower or model_lower.startswith("claude")
    except Exception:
        return False

