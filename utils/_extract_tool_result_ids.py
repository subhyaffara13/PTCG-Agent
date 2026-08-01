
def _extract_tool_result_ids(content: Any) -> Set[str]:
    if not isinstance(content, list):
        return set()
    tool_result_ids: Set[str] = set()
    for part in content:
        if not isinstance(part, dict):
            continue
        if part.get("type") != "tool_result":
            continue
        tool_use_id = part.get("tool_use_id")
        if isinstance(tool_use_id, str) and tool_use_id:
            tool_result_ids.add(tool_use_id)
    return tool_result_ids

