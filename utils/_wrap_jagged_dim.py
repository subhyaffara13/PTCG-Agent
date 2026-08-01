
def _wrap_jagged_dim(
    ndim,
    dim,
    ragged_dim,
    op_name,
    convert_to_inner_dim=True,
    allow_ragged_dim=False,
    allow_batch_dim=False,
):
    from torch._prims_common import canonicalize_dims

    wrapped = canonicalize_dims(ndim, dim)
    if wrapped == ragged_dim and not allow_ragged_dim:
        raise RuntimeError(f"{op_name}(): not supported for NestedTensor on ragged dim")
    elif wrapped == 0 and not allow_batch_dim:
        raise RuntimeError(f"{op_name}(): not supported for NestedTensor on dim=0")
    ret = (
        _outer_to_inner_dim(ndim, wrapped, ragged_dim)
        if convert_to_inner_dim
        else wrapped
    )
    if allow_batch_dim:
        # Need to disambiguate whether we're operating on the batch dim or not.
        # Operating on dim=1 -> dim=0 after the inner dim conversion.
        operating_on_batch = wrapped == 0
        return (ret, operating_on_batch)
    return ret

