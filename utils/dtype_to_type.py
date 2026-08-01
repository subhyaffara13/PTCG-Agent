
def dtype_to_type(dtype: torch.dtype) -> type:
    """
    Computes the corresponding Python type (AKA "type kind") for the
    given dtype.
    """
    if not isinstance(dtype, torch.dtype):
        raise AssertionError(f"Expected torch.dtype, got {type(dtype)}")

    if dtype is torch.bool:
        return bool
    if dtype in _integer_dtypes:
        return int
    if dtype.is_floating_point:
        return float
    if dtype in _complex_dtypes:
        return complex

    raise ValueError("Invalid dtype!")

