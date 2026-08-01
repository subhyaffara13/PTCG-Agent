
def f6(x: torch.Tensor) -> torch.Tensor:
    x = f5(x, 2)
    torch._dynamo.graph_break()
    x = f5(x, 4)
    return x


def f6(x):
    v = _f6_cache.get(x, None)
    if v is None:
        if x > 1:
            v = random()
        elif x < 1:
            v = -random()
        else:
            v = 0
        _f6_cache[x] = v
    return v


def F6(x):
    x1, x2 = x
    J0 = np.array([[-4.256, 14.7],
                   [0.8394989, 0.59964207]])
    v = np.array([(x1 + 3) * (x2**5 - 7) + 3*6,
                  np.sin(x2 * np.exp(x1) - 1)])
    return -np.linalg.solve(J0, v)

