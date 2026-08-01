
def format_user_stack_trace(
    user_stack: traceback.StackSummary | None,
) -> str:
    """
    Format the user stack trace for display in guard failure messages.

    Returns a formatted string representation of the stack trace,
    or an empty string if no user stack is available.
    """
    if user_stack is None or len(user_stack) == 0:
        return ""

    lines: list[str] = []
    for frame in user_stack:
        filename = frame.filename
        lineno = frame.lineno
        name = frame.name
        source_line = frame.line.strip() if frame.line else ""
        lines.append(f'  File "{filename}", line {lineno}, in {name}')
        if source_line:
            lines.append(f"    {source_line}")
    return "\n".join(lines)

