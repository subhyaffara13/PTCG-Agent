
def set_tensor_metadata(tensor, metadata):
    # See `get_tensor_metadata` above
    if not isinstance(metadata, dict):
        raise AssertionError(f"expected dict, got {type(metadata).__name__}")
    if not isinstance(tensor, torch.Tensor):
        raise AssertionError(f"expected torch.Tensor, got {type(tensor).__name__}")
    torch._C._set_tensor_metadata(tensor, metadata)  # type: ignore[attr-defined]

