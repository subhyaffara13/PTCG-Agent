
def is_symm_mem_enabled_for_group(group_name: c10d.GroupName) -> bool:
    """
    Check if symmetric memory is enabled for a process group.

    Args:
        group_name (str): the name of the process group.
    """
    if _is_test_mode:
        return _mocked_group_names is None or group_name in _mocked_group_names
    return group_name in _group_name_to_store

