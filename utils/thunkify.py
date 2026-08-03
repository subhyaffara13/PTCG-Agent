import functools
from typing import Callable

def thunkify(
    tracer: _ProxyTracer, f: Callable[_P, R], *args: _P.args, **kwargs: _P.kwargs
) -> Thunk[R]:
    """
    Delays computation of f until it's called again
    Also caches the result
    """
    if tracer.enable_thunkify:
        return Thunk(functools.partial(f, *args, **kwargs))
    else:
        r = f(*args, **kwargs)
        return Thunk(lambda: r)

