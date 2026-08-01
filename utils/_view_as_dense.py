
def _view_as_dense(
    tensor: torch.Tensor, Nnz: int, num_heads: int, head_dim: int
) -> torch.Tensor:
    if tensor.is_nested:
        return tensor.values()
    return tensor.view(Nnz, num_heads, head_dim)

