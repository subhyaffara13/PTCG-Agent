
def _rank_not_in_group(group: ProcessGroup | None) -> bool:
    """Check if the current process's rank is not in a given group."""
    if group is None:
        return False
    return group == GroupMember.NON_GROUP_MEMBER

