from typing import Any, Callable

def _check_out_dims_is_int_or_int_pytree(
    out_dims: out_dims_t, func: Callable[..., Any]
) -> None:
    if isinstance(out_dims, int):
        return
    tree_map_(partial(_check_int_or_none, func=func, out_dims=out_dims), out_dims)

