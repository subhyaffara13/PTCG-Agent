
def pallas_ensure_nonzero_rank(x: torch.Tensor) -> torch.Tensor:
    if len(x.shape) == 0:
        return x.reshape((1,))
    return x

