
def get_process_group_ranks(group: ProcessGroup | None) -> list[int]:
    """
    Get all ranks associated with ``group``.

    Args:
        group (Optional[ProcessGroup]): ProcessGroup to get all ranks from.
            If None, the default process group will be used.

    Returns:
        List of global ranks ordered by group rank.
    """
    return list(_world.pg_group_ranks[group or _get_default_group()].keys())

