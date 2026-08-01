
def _search_tool_names_from_object_permission(
    object_permission: Optional[LiteLLM_ObjectPermissionTable],
) -> List[str]:
    """Return allowlisted search tool names from object_permission (empty = unrestricted)."""
    if object_permission is None:
        return []
    raw = object_permission.search_tools
    if not raw:
        return []
    return list(raw)

