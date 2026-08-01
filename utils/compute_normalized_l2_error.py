
def compute_normalized_l2_error(x: torch.Tensor, y: torch.Tensor) -> torch.Tensor:
    """
    Computes the normalized L2 error between `x` and `y`.

    Args:
        x: Tensor or tuple of tensors
        y: Tensor or tuple of tensors

    Return:
        float or tuple of floats
    """

    return torch.sqrt(((x - y) ** 2).sum() / (x**2).sum())

