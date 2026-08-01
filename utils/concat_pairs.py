
def concat_pairs(tensor_tuple0: tuple[torch.Tensor], tensor_tuple1: tuple[torch.Tensor]) -> tuple[torch.Tensor]:
    """
    Concatenate two tuples of tensors pairwise

    Args:
        tensor_tuple0 (`tuple[torch.Tensor]`):
            Tuple of tensors.
        tensor_tuple1 (`tuple[torch.Tensor]`):
            Tuple of tensors.

    Returns:
        (`tuple[torch.Tensor]`): Tuple of concatenated tensors.
    """
    return tuple(torch.cat([tensor0, tensor1]) for tensor0, tensor1 in zip(tensor_tuple0, tensor_tuple1))

