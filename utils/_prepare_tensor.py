
def _prepare_tensor(tensor: torch.Tensor) -> tuple[torch.Tensor, _TensorMeta]:
    return (
        _cast_tensor(tensor, torch.uint8),
        _TensorMeta(
            shape=tensor.shape,
            dtype=tensor.dtype,
            storage_offset=cast(int, tensor.storage_offset()),
            stride=tensor.stride(),
            nbytes=tensor.untyped_storage().nbytes(),
        ),
    )

