
def is_low_precision_dtype(dtype: torch.dtype) -> bool:
    if not isinstance(dtype, torch.dtype):
        raise AssertionError(f"Expected torch.dtype, got {type(dtype)}")
    return dtype in _low_precision_dtypes

