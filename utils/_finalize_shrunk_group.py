
def _finalize_shrunk_group(
    group_info: dict, excluded_ranks_set: set, new_backend
) -> ProcessGroup:
    """Clean up old group and create new shrunk process group."""
    target_pg = group_info["process_group"]
    is_default_group = group_info["is_default_group"]

    # Handle default group dependencies - destroy other groups first
    if is_default_group:
        _destroy_all_other_groups(exclude_group=target_pg)

    # Gather original group metadata before cleanup
    original_group_metadata = _extract_group_metadata(target_pg)

    # Calculate remaining ranks efficiently
    original_ranks = get_process_group_ranks(target_pg)
    remaining_ranks = [
        rank for rank in original_ranks if rank not in excluded_ranks_set
    ]

    # Clean up the original group
    _cleanup_original_group(target_pg, is_default_group)

    # Create and configure the new process group
    new_pg = _create_shrunk_process_group(
        new_backend, remaining_ranks, original_group_metadata, is_default_group
    )

    # Register the new group in global state
    if is_default_group:
        _update_default_pg(new_pg)

    # Update global state with new group information
    rank_mapping = {
        global_rank: group_rank
        for group_rank, global_rank in enumerate(remaining_ranks)
    }
    _update_process_group_global_state(
        pg=new_pg,
        backend_name=original_group_metadata["backend_name"],
        store=original_group_metadata["store"],
        group_name=original_group_metadata["new_group_name"],
        backend_config=original_group_metadata["backend_config"],
        rank_mapping=rank_mapping,
    )

    return new_pg

