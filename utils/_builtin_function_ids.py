
def _builtin_function_ids() -> dict[int, str]:
    # See also torch/_dynamo/polyfills/loader.py, which removes items in _builtin_function_ids
    rv = {
        id(v): f"builtins.{k}"
        for k, v in builtins.__dict__.items()
        if not k.startswith("_") and callable(v)
    }
    rv.update(
        {
            id(v): f"operator.{k}"
            for k, v in operator.__dict__.items()
            if not k.startswith("_") and callable(v)
        }
    )
    return rv

