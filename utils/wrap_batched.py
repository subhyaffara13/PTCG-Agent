
def wrap_batched(
    args: tuple[Any, ...], bdims: in_dims_t, level: int
) -> tuple[Any, ...]:
    flat_args, spec = tree_flatten(args)
    flat_bdims = _broadcast_to_and_flatten(bdims, spec)
    if flat_bdims is None:
        raise AssertionError("flat_bdims must not be None")
    result = _create_batched_inputs(flat_bdims, flat_args, level, spec)
    return result

