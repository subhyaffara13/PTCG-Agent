
def is_grad_dtype(dtype: torch.dtype) -> bool:
    """
    Checks if the dtype can require a gradient.
    """
    return dtype.is_floating_point or is_complex_dtype(dtype)

