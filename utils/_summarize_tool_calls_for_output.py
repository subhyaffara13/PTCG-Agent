
def _summarize_tool_calls_for_output(tool_calls) -> str:
    """Render a tool_calls list as a compact JSON string for OUTPUT_VALUE.

    Best-effort: returns ``str(tool_calls)`` if anything unexpected happens
    so OUTPUT_VALUE is never blanked on a malformed payload.
    """
    try:
        normalized = [n for n in (_normalize_tool_call(tc) for tc in tool_calls) if n]
        return json.dumps({"tool_calls": normalized})
    except Exception:
        return str(tool_calls)

