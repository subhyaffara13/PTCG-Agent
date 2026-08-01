
def arange_like(x, dim: int) -> torch.Tensor:
    return x.new_ones(x.shape[dim]).cumsum(0) - 1

