
def _matches_claude_model_pattern(model: str) -> bool:
    """
    Check if a model string matches the Claude model naming pattern.

    Matches patterns like:
    - claude-opus-4-7
    - claude-sonnet-4-6
    - claude-haiku-4-5
    - claude-opus-5-1-20270101 (with optional date suffix)

    This allows future Claude models to be routed to the Anthropic provider
    without requiring updates to model_prices_and_context_window.json.
    """
    return _CLAUDE_PATTERN.match(model) is not None

