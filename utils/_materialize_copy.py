
def _materialize_copy(tensor: torch.Tensor, device=None, dtype=None) -> torch.Tensor:
    # This slicing is what actually loads the tensor from the safetensors slice object
    tensor = tensor[...]
    if dtype is not None or device is not None:
        tensor = tensor.to(device=device, dtype=dtype)
    return tensor

