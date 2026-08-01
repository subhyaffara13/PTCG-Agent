
def get_all_tool_calls(messages: List) -> List:
    """
    Returns extracted list of `tool_calls`.

    Done to handle openai no longer returning tool call 'name' in tool results.
    """
    tool_calls: List = []
    for m in messages:
        if m.get("tool_calls", None) is not None:
            if isinstance(m["tool_calls"], list):
                tool_calls.extend(m["tool_calls"])

    return tool_calls

