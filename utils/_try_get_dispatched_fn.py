
def _try_get_dispatched_fn(fn):
    if not callable(fn):
        return None
    return boolean_dispatched.get(fn)

