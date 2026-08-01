
def _div_aten(a, b):
    is_integral = isinstance(a, (bool, int, torch.SymInt)) or (
        isinstance(a, torch.Tensor) and utils.is_integer_dtype(a.dtype)
    )

    if is_integral:
        return torch.div(a, b, rounding_mode="trunc")
    else:
        return torch.true_divide(a, b)

