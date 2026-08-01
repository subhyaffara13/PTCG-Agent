
def static_input(x: torch.Tensor) -> torch.Tensor:
    """
    Copy and input while preserving strides
    """
    return torch.empty_strided(x.size(), x.stride(), dtype=x.dtype, device=x.device)

