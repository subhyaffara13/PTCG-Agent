
def _add_safe_globals(safe_globals: list[Callable | tuple[Callable, str]]):
    global _marked_safe_globals_set
    _marked_safe_globals_set = _marked_safe_globals_set.union(set(safe_globals))

