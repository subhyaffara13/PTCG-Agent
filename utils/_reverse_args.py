
def _reverse_args(func: UnflattenFn) -> OpTreeUnflattenFn:
    @functools.wraps(func)
    def wrapped(*args: Any, **kwargs: Any) -> Any:
        return func(*reversed(args), **kwargs)

    return wrapped

