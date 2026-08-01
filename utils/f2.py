
def f2(x: torch.Tensor) -> torch.Tensor:
    return x + 1


def f2(x):
    r"""f2 is a symmetric parabola, x**2 - 1"""
    return x**2 - 1


def f2(x):
    return 5 + (x - 2.)**6


def F2(x):
    return x


def f2(z, *params):
    x, y = z
    a, b, c, d, e, f, g, h, i, j, k, l, scale = params
    return (-g*np.exp(-((x-h)**2 + (y-i)**2) / scale))


def f2(x):
    return exp(x) - cos(x)


def f2(t, x, omega1, omega2):
    dxdt = [omega1*x[1], -omega2*x[0]]
    return dxdt


def f2(): pass

