
def _attempt_json_repair(s: str) -> Optional[Any]:
    """
    Attempt to repair truncated JSON produced by LLM tool calls.

    Handles the most common truncation patterns where the model generates
    valid JSON that is cut short (missing closing brackets/braces).

    Returns the parsed value on success, or None if repair fails.
    """
    import json

    stripped = s.rstrip()
    if not stripped:
        return None

    # Track the stack of unmatched openers to respect nesting order
    opener_stack: list = []
    in_string = False
    escape_next = False

    for ch in stripped:
        if escape_next:
            escape_next = False
            continue
        if ch == "\\":
            if in_string:
                escape_next = True
            continue
        if ch == '"':
            in_string = not in_string
            continue
        if in_string:
            continue
        if ch == "{":
            opener_stack.append("}")
        elif ch == "[":
            opener_stack.append("]")
        elif ch in ("}", "]"):
            if opener_stack and opener_stack[-1] == ch:
                opener_stack.pop()

    if not opener_stack:
        return None

    # Remove trailing comma before we close brackets
    candidate = stripped.rstrip(",")

    # Close in reverse order of opening (respects nesting)
    candidate += "".join(reversed(opener_stack))

    try:
        return json.loads(candidate)
    except json.JSONDecodeError:
        pass

    return None

