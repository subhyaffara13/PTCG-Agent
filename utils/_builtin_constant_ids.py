
def _builtin_constant_ids() -> dict[int, str]:
    """
    Collects constant builtins by eliminating callable items.
    """
    rv = {
        id(v): f"builtins.{k}"
        for k, v in builtins.__dict__.items()
        if not k.startswith("_") and not callable(v)
    }
    return rv

