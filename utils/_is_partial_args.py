
def _is_partial_args(func, args, kwargs):
    """ Like ``is_partial_args`` for builtins in our ``signatures`` registry"""
    if func not in signatures:
        return None
    sigs = signatures[func]
    return any(check_partial(sig, args, kwargs) for sig in sigs)

