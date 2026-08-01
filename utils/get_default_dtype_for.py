
def get_default_dtype_for(dtype):
    """Default scalar type given sctype category."""
    if dtype == torch.bool:
        return dtype
    if dtype.is_complex:
        return default_dtypes().complex_dtype
    if dtype.is_floating_point:
        return default_dtypes().float_dtype
    # else, it must be (some) integer
    return default_dtypes().int_dtype

