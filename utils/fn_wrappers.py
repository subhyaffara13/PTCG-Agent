
def fn_wrappers(fn: Callable[..., Any]) -> list[Callable[..., Any]]:
    fns = [fn]
    f = fn
    while hasattr(f, "__wrapped__"):
        f = f.__wrapped__
        fns.append(f)
    return fns

