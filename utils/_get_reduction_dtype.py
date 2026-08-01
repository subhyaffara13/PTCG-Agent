
def _get_reduction_dtype(input, dtype, promote_int_to_long=True):
    # if specified, dtype takes precedence
    if dtype:
        return dtype

    if input.dtype.is_floating_point or input.dtype.is_complex:
        return input.dtype
    elif promote_int_to_long:
        return torch.long

    return input.dtype

