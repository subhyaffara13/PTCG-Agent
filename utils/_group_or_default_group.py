
def _group_or_default_group(group: ProcessGroup | None = None) -> ProcessGroup:
    if group is None or group is GroupMember.WORLD:
        group = _get_default_group()
    return group

