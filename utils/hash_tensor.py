
def hash_tensor(t: torch.Tensor) -> torch.Tensor:
    """Some inexpensive hash. Used as a quick and dirty indicator for tensor mutation"""
    return t.detach().float().mean()

