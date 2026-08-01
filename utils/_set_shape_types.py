
def _set_shape_types(
    values: Sequence[ir.Value],
    meta_vals: Sequence[torch.Tensor],
    complex_to_float: bool = True,
) -> None:
    if not isinstance(meta_vals, Sequence):
        logger.warning(
            "Expected meta_vals to be a sequence, but got %s. There may be an internal error.",
            meta_vals,
        )
        meta_vals = (meta_vals,)
    for value, meta_val in zip(values, meta_vals):
        _set_shape_type(value, meta_val, complex_to_float=complex_to_float)

