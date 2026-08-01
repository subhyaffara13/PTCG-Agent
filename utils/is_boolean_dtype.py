
def is_boolean_dtype(dtype: torch.dtype) -> bool:
    if not isinstance(dtype, torch.dtype):
        raise AssertionError(f"Expected torch.dtype, got {type(dtype)}")
    return dtype is torch.bool

