
def complex_to_real_dtype(dtype: torch.dtype) -> torch.dtype:
    """Convert a complex dtype to the dtype of its real part. Return other dtypes as-is."""
    return COMPLEX_TO_REAL.get(dtype, dtype)

