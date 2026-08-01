
def enable_symm_mem_for_group(group_name: c10d.GroupName) -> None:
    """
    Enables symmetric memory for a process group.

    Args:
        group_name (str): the name of the process group.
    """
    if group_name in _group_name_to_store:
        return

    group = c10d._resolve_process_group(group_name)
    global_ranks = sorted(c10d._world.pg_group_ranks[group].keys())
    # Different subgroups with the same name should use different stores
    global_ranks_str = "_".join(map(str, global_ranks))
    store = c10d.PrefixStore(
        f"symmetric_memory-{global_ranks_str}",
        c10d._get_process_group_store(group),
    )
    _group_name_to_store[group_name] = store
    _SymmetricMemory.set_group_info(
        group_name,
        group.rank(),
        group.size(),
        store,
    )

