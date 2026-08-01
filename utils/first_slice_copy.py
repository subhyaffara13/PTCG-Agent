
def first_slice_copy(t: torch.Tensor, dim: int = 0) -> torch.Tensor:
    return torch.select_copy(t, dim, 0)

