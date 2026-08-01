
def triton_type_to_torch(dtype: str) -> torch.dtype:
    adjusted_type = _torch_triton_mapping.get(dtype, dtype)
    type_name = adjusted_type.replace("tl.", "")
    out_dtype = getattr(torch, type_name)
    assert isinstance(out_dtype, torch.dtype)
    return out_dtype

