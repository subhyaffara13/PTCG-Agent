
def is_coroutine_callable(call: typing.Callable[..., typing.Any]) -> bool:
    if inspect.isclass(call):
        return False
    if inspect.iscoroutinefunction(call):
        return True
    partial_call = isinstance(call, functools.partial) and call.func
    dunder_call = partial_call or getattr(call, "__call__", None)
    return inspect.iscoroutinefunction(dunder_call)

