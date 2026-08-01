
def f1(x: torch.Tensor) -> torch.Tensor:
    return x + 1


def f1(x):
    r"""f1 is a quadratic with roots at 0 and 1"""
    return x * (x - 1.)


def f1(x):
    return 100*(1 - x**3.)**2 + (1-x**2.) + 2*(1-x)**2.


def f1(z, *params):
    x, y = z
    a, b, c, d, e, f, g, h, i, j, k, l, scale = params
    return (a * x**2 + b * x * y + c * y**2 + d*x + e*y + f)


def f1(x):
    return x ** 2 - 2 * x - 1


def f1(x, d=0):
    """Derivatives of sin->cos->-sin->-cos."""
    if d % 4 == 0:
        return np.sin(x)
    if d % 4 == 1:
        return np.cos(x)
    if d % 4 == 2:
        return -np.sin(x)
    if d % 4 == 3:
        return -np.cos(x)


def f1(t, x, omega):
    dxdt = [omega*x[1], -omega*x[0]]
    return dxdt

