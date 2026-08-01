
def register_guard_check_spec(
    get_metadata_fn,
    eval_fn,
):
    """Attach a GuardCheckSpec to a guard method for auto-dispatch."""
    handler = GuardCheckSpec(get_metadata_fn=get_metadata_fn, eval_fn=eval_fn)

    def decorator(fn):
        fn.guard_check_spec = handler
        return fn

    return decorator

