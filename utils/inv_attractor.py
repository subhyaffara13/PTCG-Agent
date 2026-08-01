
def inv_attractor(dx, alpha: float = 300, gamma: int = 2):
    """Inverse attractor: dc = dx / (1 + alpha*dx^gamma), where dx = a - c, a = attractor point, c = bin center, dc = shift in bin center
    This is the default one according to the accompanying paper.

    Args:
        dx (`torch.Tensor`):
            The difference tensor dx = Ai - Cj, where Ai is the attractor point and Cj is the bin center.
        alpha (`float`, *optional*, defaults to 300):
            Proportional Attractor strength. Determines the absolute strength. Lower alpha = greater attraction.
        gamma (`int`, *optional*, defaults to 2):
            Exponential Attractor strength. Determines the "region of influence" and indirectly number of bin centers affected.
            Lower gamma = farther reach.

    Returns:
        torch.Tensor: Delta shifts - dc; New bin centers = Old bin centers + dc
    """
    return dx.div(1 + alpha * dx.pow(gamma))

