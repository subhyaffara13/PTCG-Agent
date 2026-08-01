
def _check_out_dims_is_int_or_int_tuple(out_dims: out_dims_t, func: Callable) -> None:
    if isinstance(out_dims, int):
        return
    if not isinstance(out_dims, tuple) or not all(
        isinstance(out_dim, int) for out_dim in out_dims
    ):
        raise ValueError(
            f"vmap({_get_name(func)}, ..., out_dims={out_dims}): `out_dims` must be "
            f"an int or a tuple of int representing where in the outputs the "
            f"vmapped dimension should appear."
        )

