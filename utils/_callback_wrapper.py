
def _callback_wrapper(cb: t.Any) -> _CallbackWrapper:
    if isinstance(cb, _CallbackWrapper):
        return cb
    else:
        return _CallbackWrapper(cb)

