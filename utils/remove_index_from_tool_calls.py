
def remove_index_from_tool_calls(
    messages: Optional[List[AllMessageValues]],
):
    if messages is not None:
        for message in messages:
            _tool_calls = message.get("tool_calls")
            if _tool_calls is not None and isinstance(_tool_calls, list):
                for tool_call in _tool_calls:
                    if (
                        isinstance(tool_call, dict) and "index" in tool_call
                    ):  # Type guard to ensure it's a dict
                        tool_call.pop("index", None)

    return

