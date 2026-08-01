
def compute_sqnr(x: torch.Tensor, y: torch.Tensor) -> torch.Tensor:
    """
    Computes the SQNR between `x` and `y`.

    Args:
        x: Tensor or tuple of tensors
        y: Tensor or tuple of tensors

    Return:
        float or tuple of floats
    """
    Ps = torch.norm(x)
    Pn = torch.norm(x - y)
    return 20 * torch.log10(Ps / Pn)

