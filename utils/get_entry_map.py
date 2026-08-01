
def get_entry_map(
    dist: _EPDistType, group: None = None
) -> dict[str, dict[str, EntryPoint]]: ...


def get_entry_map(dist: _EPDistType, group: str) -> dict[str, EntryPoint]: ...


def get_entry_map(dist: _EPDistType, group: str | None = None):
    """Return the entry point map for `group`, or the full entry map"""
    return get_distribution(dist).get_entry_map(group)

