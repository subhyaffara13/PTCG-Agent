
def to_local_if_dtensor(tensor: torch.Tensor, detach: bool = False) -> torch.Tensor:
    """Convert a DTensor to its local shard, or return a plain tensor as-is.

    When ``detach=True``, the tensor is detached before conversion —
    this applies to both DTensors and plain tensors.

    Args:
        tensor: A tensor that may be a DTensor.
        detach: If ``True``, detach before ``to_local()`` to avoid
            redistribution during backward.

    Returns:
        The local tensor component.
    """
    maybe_detached_tensor = tensor.detach() if detach else tensor
    if isinstance(maybe_detached_tensor, DTensor):
        return maybe_detached_tensor.to_local()
    return maybe_detached_tensor

