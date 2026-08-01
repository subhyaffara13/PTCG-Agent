
def get_tensor_metadata(tensor):
    # Tensor's Metadata for serializing.
    # Currently, this only returns a dict[string, bool] specifying whether
    # `conj` or `neg` bit is set.
    if not isinstance(tensor, torch.Tensor):
        raise AssertionError(f"expected torch.Tensor, got {type(tensor).__name__}")
    return torch._C._get_tensor_metadata(tensor)  # type: ignore[attr-defined]

