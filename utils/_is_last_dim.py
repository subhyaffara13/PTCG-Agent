
def _is_last_dim(t: torch.Tensor, dim: int) -> bool:
    return dim == t.ndim - 1 or dim == -1

