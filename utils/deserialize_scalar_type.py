
def deserialize_scalar_type(st: ScalarType) -> torch.dtype:
    return _SERIALIZE_TO_TORCH_DTYPE[st]

