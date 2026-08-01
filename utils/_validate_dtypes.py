
def _validate_dtypes(*dtypes):
    for dtype in dtypes:
        if not isinstance(dtype, torch.dtype):
            raise AssertionError(f"Expected dtype to be torch.dtype, got {type(dtype)}")
    return dtypes

