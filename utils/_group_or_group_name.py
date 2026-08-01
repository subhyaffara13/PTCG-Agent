
def _group_or_group_name(
    group: dist.ProcessGroup | c10d.GroupName,
) -> dist.ProcessGroup | c10d.GroupName:
    if isinstance(group, str):
        return group
    elif dist.config.compile_on_one_rank:
        return group
    else:
        return group.group_name

