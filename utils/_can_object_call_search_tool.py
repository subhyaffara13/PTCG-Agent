from typing import List

def _can_object_call_search_tool(
    search_tool_name: str,
    allowed_search_tools: List[str],
    object_type: Literal["key", "team", "project"],
) -> Literal[True]:
    """
    Check if an object (key/team/project) can access a specific search tool.

    Similar to _can_object_call_model but for search tools.

    Args:
        search_tool_name: The search tool being requested
        allowed_search_tools: List of allowed search tool names for this object
        object_type: Type of object for error messaging

    Returns:
        True if access is allowed

    Raises:
        ProxyException if access is denied
    """
    # Empty list means all search tools are allowed
    if not allowed_search_tools:
        return True

    # Check if the search tool is in the allowlist
    if search_tool_name in allowed_search_tools:
        return True

    # Access denied
    raise ProxyException(
        message=f"{object_type.capitalize()} not allowed to access search tool: {search_tool_name}. "
        f"Allowed search tools: {allowed_search_tools}",
        type=ProxyErrorTypes.key_model_access_denied,
        param="search_tool_name",
        code=status.HTTP_403_FORBIDDEN,
    )

