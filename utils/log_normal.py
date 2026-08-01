
def log_normal(self, mean=1, std=2, generator=None):
    if generator is not None:
        raise AssertionError("generator is not supported in refs")
    torch._check(
        not utils.is_complex_dtype(self.dtype)
        and not utils.is_integer_dtype(self.dtype)
        and not utils.is_boolean_dtype(self.dtype),
        lambda: f"log_normal not implemented for {self.dtype}",
    )
    torch._check(
        0 < std,
        lambda: f"log_normal_ expects std > 0.0, but found std={std}",
    )
    return torch.exp(std * torch.randn_like(self) + mean)


def LogNormal(name, mean, std):
    r"""
    Create a continuous random variable with a log-normal distribution.

    Explanation
    ===========

    The density of the log-normal distribution is given by

    .. math::
        f(x) := \frac{1}{x\sqrt{2\pi\sigma^2}}
                e^{-\frac{\left(\ln x-\mu\right)^2}{2\sigma^2}}

    with :math:`x \geq 0`.

    Parameters
    ==========

    mu : Real number
        The log-scale.
    sigma : Real number
        A shape. ($\sigma^2 > 0$)

    Returns
    =======

    RandomSymbol

    Examples
    ========

    >>> from sympy.stats import LogNormal, density
    >>> from sympy import Symbol, pprint

    >>> mu = Symbol("mu", real=True)
    >>> sigma = Symbol("sigma", positive=True)
    >>> z = Symbol("z")

    >>> X = LogNormal("x", mu, sigma)

    >>> D = density(X)(z)
    >>> pprint(D, use_unicode=False)
                          2
           -(-mu + log(z))
           -----------------
                      2
      ___      2*sigma
    \/ 2 *e
    ------------------------
            ____
        2*\/ pi *sigma*z


    >>> X = LogNormal('x', 0, 1) # Mean 0, standard deviation 1

    >>> density(X)(z)
    sqrt(2)*exp(-log(z)**2/2)/(2*sqrt(pi)*z)

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Lognormal
    .. [2] https://mathworld.wolfram.com/LogNormalDistribution.html

    """

    return rv(name, LogNormalDistribution, (mean, std))

