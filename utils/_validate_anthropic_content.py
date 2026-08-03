from typing import Any

def _validate_anthropic_content(content: Mapping[str, Any]) -> type:
    """
    Validate and determine which Anthropic TypedDict applies.

    Returns the corresponding TypedDict class if recognized, otherwise raises.
    """
    content_type = content.get("type")
    if not content_type:
        raise ValueError("Anthropic content missing required field: 'type'")

    mapping = {
        "tool_use": AnthropicMessagesToolUseParam,
        "tool_result": AnthropicMessagesToolResultParam,
    }

    expected_cls = mapping.get(content_type)
    if expected_cls is None:
        raise ValueError(f"Unknown Anthropic content type: '{content_type}'")

    missing = [
        k for k in getattr(expected_cls, "__required_keys__", set()) if k not in content
    ]
    if missing:
        raise ValueError(
            f"Missing required fields in {content_type} block: {', '.join(missing)}"
        )

    return expected_cls

