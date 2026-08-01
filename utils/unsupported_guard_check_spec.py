
def unsupported_guard_check_spec(fn):
    """Mark a guard method as unsupported for auto-cache dispatch."""
    fn.guard_check_spec = UnsupportedGuardCheckSpec(fn.__name__)
    return fn

