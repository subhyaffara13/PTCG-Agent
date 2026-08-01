
def _extract_tool_use_ids(content: Any) -> List[str]:
    if not isinstance(content, list):
        return []
    tool_use_ids: List[str] = []
    for part in content:
        if not isinstance(part, dict):
            continue
        if part.get("type") != "tool_use":
            continue
        tool_use_id = part.get("id")
        if isinstance(tool_use_id, str) and tool_use_id:
            tool_use_ids.append(tool_use_id)
    return tool_use_ids

