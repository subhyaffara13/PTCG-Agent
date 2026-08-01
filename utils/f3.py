
def f3(x: torch.Tensor) -> torch.Tensor:
    return f2(x)


def f3(x):
    r"""A quartic with roots at 0, 1, 2 and 3"""
    return x * (x - 1.) * (x - 2.) * (x - 3.)  # x**4 - 6x**3 + 11x**2 - 6x


def f3(x):
    xp = array_namespace(x)
    return xp.exp(x) - 5*x


def F3(x):
    A = np.array([[-2, 1, 0.], [1, -2, 1], [0, 1, -2]])
    b = np.array([1, 2, 3.])
    return A @ x - b


def f3(z, *params):
    x, y = z
    a, b, c, d, e, f, g, h, i, j, k, l, scale = params
    return (-j*np.exp(-((x-k)**2 + (y-l)**2) / scale))

