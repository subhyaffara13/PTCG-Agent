
def _remove_safe_globals(
    globals_to_remove: list[Callable | tuple[Callable, str]],
):
    global _marked_safe_globals_set
    _marked_safe_globals_set = _marked_safe_globals_set - set(globals_to_remove)

