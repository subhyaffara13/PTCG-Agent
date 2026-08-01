
def int_to_valid_dtype(val: int) -> torch.dtype:
    from torch._export.converter import _TORCH_ENUM_TO_DTYPE  # No circular import.

    if isinstance(val, torch.dtype):
        return val
    dtype = _TORCH_ENUM_TO_DTYPE[val]
    if dtype == torch.quint8:
        return torch.uint8
    elif dtype == torch.qint8:
        return torch.int8
    return dtype

