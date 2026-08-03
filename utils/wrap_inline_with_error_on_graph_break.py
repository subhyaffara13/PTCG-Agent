from typing import Callable

def wrap_inline_with_error_on_graph_break(
    fn: Callable[_P, _R], error_on_graph_break: bool
) -> Callable[_P, _R]:
    # NB: need multiple definitions in order to prevent `fullgraph` from
    # being a freevar of wrapper
    # NOTE: do not functools.wraps(fn) because we don't ever want these wrappers to be skipped!
    if error_on_graph_break:

        def wrapper(*args: _P.args, **kwargs: _P.kwargs) -> _R:
            with torch._dynamo.error_on_graph_break(True):
                return fn(*args, **kwargs)

    else:

        def wrapper(*args: _P.args, **kwargs: _P.kwargs) -> _R:
            with torch._dynamo.error_on_graph_break(False):
                return fn(*args, **kwargs)

    return wrapper

