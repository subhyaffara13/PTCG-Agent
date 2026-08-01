
def full_like_impl(
    input: ComplexTensor,
    fill_value: complex,
    *args: Any,
    dtype: torch.dtype | None = None,
    **kwargs: Any,
) -> torch.Tensor | ComplexTensor:
    # Note: Cannot be merged with the cases below due to the `fill_value` argument
    input_r, input_i = split_complex_tensor(input)
    if dtype is not None and dtype not in COMPLEX_TO_REAL:
        return torch.full_like(input_r, fill_value, *args, dtype=dtype, **kwargs)

    if dtype is not None:
        kwargs["dtype"] = COMPLEX_TO_REAL[dtype]

    fv_r, fv_i = split_complex_arg(fill_value)
    ret_r = torch.full_like(input_r, fv_r, *args, **kwargs)
    ret_i = torch.full_like(input_i, fv_i, *args, **kwargs)

    return ComplexTensor(ret_r, ret_i)

