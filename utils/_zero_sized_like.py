
def _zero_sized_like(tensor: torch.Tensor, dim: int) -> torch.Tensor:
    tensor_size = list(tensor.size())
    tensor_size[dim] = 0
    empty_tensor = torch.empty(*tensor_size, dtype=tensor.dtype, device=tensor.device)
    return empty_tensor

