
def triton_compute_type(dtype: torch.dtype) -> str:
    """Convert torch.dtype to triton type and upcast [b]float16 to float32"""
    return triton_type(upcast_compute_type(dtype))

