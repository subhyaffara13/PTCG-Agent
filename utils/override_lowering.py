import functools
from typing import Any, Callable

def override_lowering(
    aten_op: Callable[..., Any], override_fn: Callable[..., Any]
) -> Iterator[None]:
    """
    Override the lowering of aten_op with override_fn.
    The first argument of override_fn is the original lowering fn.
    """
    from torch._inductor import lowering

    orig_fn = lowering.lowerings[aten_op]
    try:
        lowering.lowerings[aten_op] = functools.partial(override_fn, orig_fn)
        yield
    finally:
        lowering.lowerings[aten_op] = orig_fn

