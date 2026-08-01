
def triton_acc_type(dtype: torch.dtype) -> str:
    """Convert torch.dtype to triton type, with reduction upcasts"""
    return triton_compute_type(upcast_acc_dtype(dtype))

