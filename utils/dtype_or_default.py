
def dtype_or_default(dtype: torch.dtype | None) -> torch.dtype:
    return dtype if dtype is not None else torch.get_default_dtype()

