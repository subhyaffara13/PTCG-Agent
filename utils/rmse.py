
def rmse(ref: torch.Tensor, res: torch.Tensor) -> torch.Tensor:
    """
    Calculate root mean squared error
    """
    return torch.sqrt(torch.mean(torch.square(ref - res)))

