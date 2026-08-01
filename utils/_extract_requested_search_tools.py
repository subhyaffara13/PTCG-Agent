
def _extract_requested_search_tools(object_permission: Optional[dict]) -> List[str]:
    """Return search_tool_name values from a key's object_permission dict."""
    if not object_permission or not isinstance(object_permission, dict):
        return []
    raw = object_permission.get("search_tools")
    if not isinstance(raw, list):
        return []
    return [str(x) for x in raw if x]

