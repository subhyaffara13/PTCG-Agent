
def masked_mean(mask: torch.Tensor, value: torch.Tensor, dim: int, eps: float = 1e-4) -> torch.Tensor:
    mask = mask.expand(*value.shape)
    return torch.sum(mask * value, dim=dim) / (eps + torch.sum(mask, dim=dim))

