
def parse_tool_call_arguments(
    arguments: Optional[str],
    tool_name: Optional[str] = None,
    context: Optional[str] = None,
) -> Any:
    """
    Parse tool call arguments from a JSON string.

    When the JSON is malformed (e.g. truncated by the model), this function
    attempts a lightweight repair (closing unmatched brackets/braces) before
    raising an error.  A warning is logged whenever repair succeeds so that
    callers are aware the arguments were not perfectly formed.

    Args:
        arguments: The JSON string containing tool arguments, or None.
        tool_name: Optional name of the tool (for error messages).
        context: Optional context string (e.g., "Anthropic Messages API").

    Returns:
        Parsed arguments (usually a dict, but may be any JSON-deserializable
        type such as list, str, int, float, or None).  Returns empty dict if
        arguments is None or empty.

    Raises:
        ValueError: If the arguments string is not valid JSON and cannot be repaired.
    """
    import json

    if not arguments or not arguments.strip():
        return {}

    try:
        return json.loads(arguments)
    except json.JSONDecodeError as original_error:
        repaired = _attempt_json_repair(arguments)
        if repaired is not None:
            verbose_logger.warning(
                "Repaired truncated tool call arguments for tool '%s' (%s). "
                "Original (%d chars): %.200s%s",
                tool_name or "<unknown>",
                context or "unknown context",
                len(arguments),
                arguments,
                "..." if len(arguments) > 200 else "",
            )
            return repaired

        error_parts = ["Failed to parse tool call arguments"]

        if tool_name:
            error_parts.append(f"for tool '{tool_name}'")
        if context:
            error_parts.append(f"({context})")

        error_message = (
            " ".join(error_parts)
            + f". Error: {str(original_error)}. Arguments: {arguments}"
        )

        raise ValueError(error_message) from original_error

