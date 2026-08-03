from typing import Any, Callable

def _avgpool_helper(
    tuple_fn: Callable[[Any], Sequence[int]],
    padding: int | Sequence[int],
    kernel_size,
    stride,
    divisor_override,
    name,
) -> tuple[int, ...]:
    if divisor_override and divisor_override.node().kind() != "prim::Constant":
        _unimplemented(name, "divisor_override")
    return tuple(tuple_fn(padding))

