
def skip_guard_check_spec(fn):
    """Mark a guard method as skipped during auto-cache dispatch."""
    fn.guard_check_spec = SKIP_GUARD
    return fn

