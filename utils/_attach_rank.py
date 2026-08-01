
def _attach_rank(tensor: torch.Tensor, rank: int) -> torch.Tensor:
    """
    Attaches rank as an attribute to given tensor so that the send or recv implementation
    knows which rank initiates the operation (note under local tensor mode ).
    """
    from torch.distributed.tensor import DTensor

    if isinstance(tensor, DTensor):
        tensor = tensor._local_tensor

    tensor.__src_rank__ = rank  # type: ignore[attr-defined]
    return tensor

