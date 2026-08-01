
def _broadcast_to_dim(x: Tensor, dim: int) -> Tensor:
    while x.dim() < dim:
        x = x.unsqueeze(0)
    return x

