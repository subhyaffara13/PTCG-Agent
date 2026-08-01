
def _mvdigamma(x: Tensor, p: int) -> Tensor:
    if not x.gt((p - 1) / 2).all():
        raise AssertionError("Wrong domain for multivariate digamma function.")
    return torch.digamma(
        x.unsqueeze(-1)
        - torch.arange(p, dtype=x.dtype, device=x.device).div(2).expand(x.shape + (-1,))
    ).sum(-1)

