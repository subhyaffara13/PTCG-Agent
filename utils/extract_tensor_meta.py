
def extract_tensor_meta(tensor: torch.Tensor) -> TensorMeta:
    """Extract metadata from a tensor.

    Handles both plain Tensor and DTensor correctly: DTensors are
    dispatched to ``_DTensorMeta.from_dtensor`` which captures local
    shard attributes plus global shape/placement info, while plain
    tensors use ``_TensorMeta.from_tensor``.

    Args:
        tensor: A plain tensor or DTensor.

    Returns:
        ``_TensorMeta`` for plain tensors, ``_DTensorMeta`` for DTensors.
    """
    if isinstance(tensor, DTensor):
        return _DTensorMeta.from_dtensor(tensor)
    else:
        return _TensorMeta.from_tensor(tensor)

