
def _register_builtin(fn, op) -> None:
    _get_builtin_table()[id(fn)] = op

