
def f5(x: torch.Tensor, n: int) -> torch.Tensor:
    if torch.compiler.is_compiling():
        return x + n
    return x


def f5(x):
    r"""
    Hyperbola with a pole at x=1, but pole replaced with 0. Not continuous at root.
    """
    if x != 1:
        return 1.0 / (1. - x)
    return 0


def f5(x):
    return 8*x**3 - 2*x**2 - 7*x + 3


def F5(x):
    return pressure_network(x, 4, np.array([.5, .5, .5, .5]))

