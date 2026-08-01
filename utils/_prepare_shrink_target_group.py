
def _prepare_shrink_target_group(group: ProcessGroup | None) -> dict:
    """Prepare and validate the target group for shrinking."""
    target_pg = group if group is not None else _get_default_group()

    # Cache frequently accessed properties to avoid repeated calls
    group_size = int(target_pg.size())
    group_info = {
        "process_group": target_pg,
        "is_default_group": (target_pg == _get_default_group()),
        "group_size": group_size,
        "current_rank": target_pg.rank(),
        "group_name": _get_process_group_name(target_pg),
    }

    # Validate that we have a valid process group
    if group_size <= 1:
        raise ValueError(
            f"Cannot shrink a process group with size {group_size}. "
            f"Group must have at least 2 ranks to support shrinking."
        )

    return group_info

