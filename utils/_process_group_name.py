
def _process_group_name(ranks, use_hashed_name) -> GroupName:
    # Create name for a process group.
    global _world
    if use_hashed_name:
        pg_name = GroupName(_hash_ranks_to_str(ranks))
    else:
        pg_name = GroupName(str(_world.group_count))
        _world.group_count += 1
    # TODO: why is group count incremented only in the else path?
    return pg_name

