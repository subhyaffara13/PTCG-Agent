
def upcast_acc_dtype(dtype: torch.dtype) -> torch.dtype:
    """Implicit upcasts used for Triton reduction types"""
    if is_integer_dtype(dtype) and dtype.is_signed and dtype.itemsize <= 4:
        return torch.int32
    return upcast_compute_type(dtype)

