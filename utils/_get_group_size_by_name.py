
def _get_group_size_by_name(group_name: GroupName | ProcessGroup) -> int:
    if isinstance(group_name, str):
        # pyrefly: ignore[bad-argument-type]  # pyrefly bug
        group_name = _resolve_process_group(group_name)
    return group_name.size()

