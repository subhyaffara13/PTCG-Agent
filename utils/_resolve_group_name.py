
def _resolve_group_name(group: RANK_TYPES, tag: str = "") -> c10d.GroupName:
    """
    Given group in RANK_TYPES, return the group name.
    """
    group = _resolve_group(group, tag)
    if isinstance(group, str):
        return c10d.GroupName(group)
    else:
        return group.group_name

