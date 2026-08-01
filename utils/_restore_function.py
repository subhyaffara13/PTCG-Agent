
def _restore_function(fn: Callable, fn_module: types.ModuleType) -> None:
    """Restore the function that is replaced by _distribute_function."""
    if fn not in _replaced_functions:
        return

    original_name, original_fn = _replaced_functions[fn]
    setattr(fn_module, original_name, original_fn)

