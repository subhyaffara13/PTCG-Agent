from typing import Any, Callable

def foreach_map(op: Callable, *operands: Any, **kwargs: dict[str, Any]):
    from torch._dynamo.polyfills import foreach_map_fn

    return _foreach_map(foreach_map_fn, op, *operands, **kwargs)

