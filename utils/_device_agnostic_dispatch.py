
def _device_agnostic_dispatch(device: str, dispatch_table: dict[str, Callable], *args, **kwargs):
    if device not in dispatch_table:
        if not callable(dispatch_table["default"]):
            return dispatch_table["default"]

        return dispatch_table["default"](*args, **kwargs)

    fn = dispatch_table[device]

    # Some device agnostic functions return values or None, will return then directly.
    if not callable(fn):
        return fn

    return fn(*args, **kwargs)

