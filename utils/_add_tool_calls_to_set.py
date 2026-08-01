
def _add_tool_calls_to_set(tool_calls: Any, out: Set[str]) -> None:
    """Extract tool names from OpenAI-style tool_calls list into out."""
    if not isinstance(tool_calls, list):
        return
    for tc in tool_calls:
        if not isinstance(tc, dict):
            continue
        fn = tc.get("function")
        if isinstance(fn, dict):
            name = fn.get("name")
            if name and isinstance(name, str) and name.strip():
                out.add(name.strip())

