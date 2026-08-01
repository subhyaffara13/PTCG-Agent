
def _rewrite_sin(m_n, s, a, b):
    """
    Re-write the sine function ``sin(m*s + n)`` as gamma functions, compatible
    with the strip (a, b).

    Return ``(gamma1, gamma2, fac)`` so that ``f == fac/(gamma1 * gamma2)``.

    Examples
    ========

    >>> from sympy.integrals.transforms import _rewrite_sin
    >>> from sympy import pi, S
    >>> from sympy.abc import s
    >>> _rewrite_sin((pi, 0), s, 0, 1)
    (gamma(s), gamma(1 - s), pi)
    >>> _rewrite_sin((pi, 0), s, 1, 0)
    (gamma(s - 1), gamma(2 - s), -pi)
    >>> _rewrite_sin((pi, 0), s, -1, 0)
    (gamma(s + 1), gamma(-s), -pi)
    >>> _rewrite_sin((pi, pi/2), s, S(1)/2, S(3)/2)
    (gamma(s - 1/2), gamma(3/2 - s), -pi)
    >>> _rewrite_sin((pi, pi), s, 0, 1)
    (gamma(s), gamma(1 - s), -pi)
    >>> _rewrite_sin((2*pi, 0), s, 0, S(1)/2)
    (gamma(2*s), gamma(1 - 2*s), pi)
    >>> _rewrite_sin((2*pi, 0), s, S(1)/2, 1)
    (gamma(2*s - 1), gamma(2 - 2*s), -pi)
    """
    # (This is a separate function because it is moderately complicated,
    #  and I want to doctest it.)
    # We want to use pi/sin(pi*x) = gamma(x)*gamma(1-x).
    # But there is one complication: the gamma functions determine the
    # integration contour in the definition of the G-function. Usually
    # it would not matter if this is slightly shifted, unless this way
    # we create an undefined function!
    # So we try to write this in such a way that the gammas are
    # eminently on the right side of the strip.
    m, n = m_n

    m = expand_mul(m/pi)
    n = expand_mul(n/pi)
    r = ceiling(-m*a - n.as_real_imag()[0])  # Don't use re(n), does not expand
    return gamma(m*s + n + r), gamma(1 - n - r - m*s), (-1)**r*pi

