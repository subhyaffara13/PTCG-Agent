
def _check_int_or_none(x: Any, func: Callable[..., Any], out_dims: out_dims_t) -> None:
    if isinstance(x, int):
        return
    if x is None:
        return
    raise ValueError(
        f"vmap({_get_name(func)}, ..., out_dims={out_dims}): `out_dims` must be "
        f"an int, None or a python collection of ints representing where in the outputs the "
        f"vmapped dimension should appear."
    )

