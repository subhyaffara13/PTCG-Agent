
def _update_process_group_global_state(
    pg: ProcessGroup,
    backend_name: str,
    store: Store,
    group_name: GroupName,
    backend_config: str,
    rank_mapping: dict[int, int] | None = None,
    pg_tag: str | None = None,
    user_tag: str | None = None,
) -> None:
    """
    Update all global state dictionaries for a process group.

    This helper function consolidates the common pattern of updating multiple
    global state dictionaries when creating or modifying process groups.

    Args:
        pg (ProcessGroup): The process group to update state for.
        backend_name (str): Backend name for pg_map.
        store (Store): Store instance for pg_map.
        group_name (str): Group name for pg_names and registration.
        backend_config (str): Backend configuration string.
        rank_mapping (Dict[int, int], optional): Global rank to group rank mapping.
            If None, skips updating pg_group_ranks.
        pg_tag (str, optional): Process group tag. If None, defaults to f"ptd:{group_name}".
        user_tag (str, optional): User-provided tag for special tag handling.
            If provided, creates "user:{user_tag}" tag and also adds to default "".
    """
    # Update main process group mappings
    _world.pg_map[pg] = (backend_name, store)
    _world.pg_names[pg] = group_name
    _world.pg_backend_config[pg] = backend_config

    # Register the process group name
    _register_process_group(group_name, pg)

    # Update rank mapping if provided
    if rank_mapping is not None:
        _world.pg_group_ranks[pg] = rank_mapping

    # Handle tag management
    if pg_tag is None:
        pg_tag = f"ptd:{group_name}"

    if user_tag is not None:
        # Special handling for user-provided tags
        # Add to default "" tag first
        _world.tags_to_pg.setdefault("", []).append(pg)
        # Then create user-specific tag
        user_pg_tag = f"user:{user_tag}"
        _world.tags_to_pg.setdefault(user_pg_tag, []).append(pg)
        _world.pg_to_tag[pg] = user_pg_tag
    else:
        # Standard process group tag
        _world.tags_to_pg.setdefault(pg_tag, []).append(pg)
        _world.pg_to_tag[pg] = pg_tag

