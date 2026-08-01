
def triton_type(dtype: torch.dtype) -> str:
    """Convert torch.dtype to triton type"""
    triton_type_name = _triton_type_re.sub("tl.", str(dtype))
    return _triton_type_mapping.get(triton_type_name, triton_type_name)

