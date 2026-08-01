
def _tensor_or_tensors_to_tuple(
    tensors: _TensorOrOptionalTensors | None, length: int
) -> tuple[_OptionalTensor, ...]:
    if tensors is None:
        return (None,) * length
    if isinstance(tensors, torch.Tensor):
        return (tensors,)
    return tuple(tensors)

