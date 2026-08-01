
def parse_jsonl_with_embedded_newlines(content: str) -> List[dict]:
    """
    Parse JSONL content that may contain JSON objects with embedded newlines in string values.

    Unlike splitlines(), this function properly handles cases where JSON string values
    contain literal newline characters, which would otherwise break simple line-based parsing.

    Args:
        content: The JSONL file content as a string

    Returns:
        List of parsed JSON objects

    Example:
        >>> content = '{"id":1,"msg":"Line 1\\nLine 2"}\\n{"id":2,"msg":"test"}'
        >>> parse_jsonl_with_embedded_newlines(content)
        [{"id":1,"msg":"Line 1\\nLine 2"}, {"id":2,"msg":"test"}]
    """
    json_objects = []
    buffer = ""

    for char in content:
        buffer += char
        if char == "\n":
            # Try to parse what we have so far
            try:
                json_object = json.loads(buffer.strip())
                json_objects.append(json_object)
                buffer = ""  # Reset buffer for next JSON object
            except json.JSONDecodeError:
                # Not a complete JSON object yet, keep accumulating
                continue

    # Handle any remaining content in buffer
    if buffer.strip():
        try:
            json_object = json.loads(buffer.strip())
            json_objects.append(json_object)
        except json.JSONDecodeError as e:
            verbose_logger.error(
                f"error parsing final buffer: {buffer[:100]}..., error: {e}"
            )
            raise e

    return json_objects

