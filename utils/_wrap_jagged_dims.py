
def _wrap_jagged_dims(ndim, dims, op_name, ragged_idx=1):
    """
    For NestedTensor operators,
    wraps dimensions to non-negative values,
    and returns metadata related to reduction dimension(s).
    """
    from torch._prims_common import canonicalize_dims

    if not isinstance(dims, (tuple, list)):
        raise AssertionError(
            f"_wrap_jagged_dims(): cannot iterate over dimensions of type {type(dims)}"
        )

    wrapped_dims = [
        canonicalize_dims(ndim, d) for d in dims
    ]  # convert all indices to non-negative values

    operate_on_batch = 0 in wrapped_dims
    operate_on_ragged = ragged_idx in wrapped_dims
    operate_on_non_batch = any(d != 0 and d != ragged_idx for d in wrapped_dims)

    # ensure no duplicates, which can result from both batch and ragged mapping to 0
    outer_to_inner_dim = tuple(
        dict.fromkeys(_outer_to_inner_dim(ndim, d, ragged_idx) for d in wrapped_dims)
    )

    return outer_to_inner_dim, operate_on_batch, operate_on_ragged, operate_on_non_batch

