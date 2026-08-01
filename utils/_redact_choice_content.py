
def _redact_choice_content(choice):
    """Helper to redact content in a choice (message or delta)."""
    if isinstance(choice, litellm.Choices):
        choice.message.content = "redacted-by-litellm"
        if hasattr(choice.message, "reasoning_content"):
            choice.message.reasoning_content = "redacted-by-litellm"
        if hasattr(choice.message, "thinking_blocks"):
            choice.message.thinking_blocks = None
    elif isinstance(choice, litellm.utils.StreamingChoices):
        choice.delta.content = "redacted-by-litellm"
        if hasattr(choice.delta, "reasoning_content"):
            choice.delta.reasoning_content = "redacted-by-litellm"
        if hasattr(choice.delta, "thinking_blocks"):
            choice.delta.thinking_blocks = None

