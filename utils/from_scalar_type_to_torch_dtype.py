
def from_scalar_type_to_torch_dtype(scalar_type: type) -> torch.dtype | None:
    return _SCALAR_TYPE_TO_TORCH_DTYPE.get(scalar_type)

