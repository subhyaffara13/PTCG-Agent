
def std_mean(
    a: TensorLikeType,
    dim: DimsType | None = None,
    *,
    unbiased: bool | None = None,
    keepdim: bool = False,
    correction: NumberType | None = None,
):
    dim, unbiased = _dim_var_dispatch(dim, unbiased)
    correction = utils.set_correction(unbiased, correction)
    opmath_dtype, dtype = utils.reduction_dtypes(
        a, REDUCTION_OUTPUT_TYPE_KIND.COMPLEX_TO_FLOAT
    )
    original_dtype = a.dtype
    a = _maybe_convert_to_dtype(a, opmath_dtype)
    a_var, a_mean = torch.var_mean(a, dim, correction=correction, keepdim=keepdim)
    a_std = torch.sqrt(a_var)
    if dtype is None:
        raise AssertionError("dtype should not be None after reduction_dtypes")
    return (
        _maybe_convert_to_dtype(a_std, dtype),
        _maybe_convert_to_dtype(a_mean, original_dtype),
    )


def std_mean(g: jit_utils.GraphContext, input, *args):
    var, mean = var_mean(g, input, *args)
    return g.op("Sqrt", var), mean

