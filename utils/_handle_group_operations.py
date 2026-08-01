
def _handle_group_operations(
    op_type: str, value: Any, teams_set: Set[str]
) -> Optional[Set[str]]:
    """Handle group/team membership operations."""
    group_values = _extract_group_values(value)
    if op_type == "replace":
        return set(group_values)
    elif op_type == "add":
        teams_set.update(group_values)
    elif op_type == "remove":
        for gid in group_values:
            teams_set.discard(gid)
    return None

