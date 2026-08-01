
def get_entry_info(dist: _EPDistType, group: str, name: str) -> EntryPoint | None:
    """Return the EntryPoint object for `group`+`name`, or ``None``"""
    return get_distribution(dist).get_entry_info(group, name)

