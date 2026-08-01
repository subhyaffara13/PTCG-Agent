
def _canonicalize_group_rank(
    group: ProcessGroup,
    global_rank: int | None = None,
    group_rank: int | None = None,
    return_global: bool = False,
) -> int:
    """
    Helper method to take _either_ a global rank or a group rank and produce a group rank.

    If 'return_global' is true, produce a global rank instead of a group rank.
    """

    if group_rank is not None:
        if global_rank is not None:
            raise ValueError("Can't specify both group_rank and global_rank")
        if return_global:
            return get_global_rank(group, group_rank)
    else:
        if global_rank is None:
            raise ValueError("Must specify global_rank or group_rank")
        if return_global:
            return global_rank
        group_rank = get_group_rank(group, global_rank)
    return group_rank

