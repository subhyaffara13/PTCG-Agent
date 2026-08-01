
def f4(x: torch.Tensor) -> torch.Tensor:
    x = f5(x, 1)
    x = torch._dynamo.dont_skip_tracing(f6)(x)
    x = f5(x, 8)
    return x


def f4(x):
    r"""Piecewise linear, left- and right- discontinuous at x=1, the root."""
    if x > 1:
        return 1.0 + .1 * x
    if x < 1:
        return -1.0 + .1 * x
    return 0


def f4(x):
    return x**5. - 5*x**3. - 20.*x + 5.

