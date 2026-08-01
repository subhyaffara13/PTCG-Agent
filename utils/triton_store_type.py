
def triton_store_type(dtype: torch.dtype) -> str:
    """Convert torch.dtype to triton type, with fix for storing tl.bool"""
    if dtype == torch.bool:
        dtype = torch.int8
    return triton_type(dtype)

