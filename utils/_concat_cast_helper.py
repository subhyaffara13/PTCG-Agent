
def _concat_cast_helper(tensors, out=None, dtype=None, casting="same_kind"):
    """Figure out dtypes, cast if necessary."""

    if out is not None or dtype is not None:
        # figure out the type of the inputs and outputs
        out_dtype = out.dtype.torch_dtype if dtype is None else dtype
    else:
        out_dtype = _dtypes_impl.result_type_impl(*tensors)

    # cast input arrays if necessary; do not broadcast them against `out`
    tensors = _util.typecast_tensors(tensors, out_dtype, casting)

    return tensors

