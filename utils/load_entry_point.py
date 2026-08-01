
def load_entry_point(dist: _EPDistType, group: str, name: str) -> _ResolvedEntryPoint:
    """Return `name` entry point of `group` for `dist` or raise ImportError"""
    return get_distribution(dist).load_entry_point(group, name)

