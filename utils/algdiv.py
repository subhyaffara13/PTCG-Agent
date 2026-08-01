
def algdiv(a: ArrayLike, b: ArrayLike) -> Array:
    """
    Compute ``log(gamma(a))/log(gamma(a + b))`` when ``b >= 8``.

    Derived from scipy's implementation of `algdiv`_.

    This differs from the scipy implementation in that it assumes a <= b
    because recomputing ``a, b = jnp.minimum(a, b), jnp.maximum(a, b)`` might
    be expensive and this is only called by ``betaln``.

    .. _algdiv:
        https://github.com/scipy/scipy/blob/c89dfc2b90d993f2a8174e57e0cbc8fbe6f3ee19/scipy/special/cdflib/algdiv.f
    """
    c0 = 0.833333333333333e-01
    c1 = -0.277777777760991e-02
    c2 = 0.793650666825390e-03
    c3 = -0.595202931351870e-03
    c4 = 0.837308034031215e-03
    c5 = -0.165322962780713e-02
    h = a / b
    c = h / (1 + h)
    x = h / (1 + h)
    d = b + (a - 0.5)
    # Set sN = (1 - x**n)/(1 - x)
    x2 = x * x
    s3 = 1.0 + (x + x2)
    s5 = 1.0 + (x + x2 * s3)
    s7 = 1.0 + (x + x2 * s5)
    s9 = 1.0 + (x + x2 * s7)
    s11 = 1.0 + (x + x2 * s9)
    # Set w = del(b) - del(a + b)
    # where del(x) is defined by ln(gamma(x)) = (x - 0.5)*ln(x) - x + 0.5*ln(2*pi) + del(x)
    t = (1.0 / b) ** 2
    w = ((((c5 * s11 * t + c4 * s9) * t + c3 * s7) * t + c2 * s5) * t + c1 * s3) * t + c0
    w = w * (c / b)
    # Combine the results
    u = d * lax.log1p(a / b)
    v = a * (lax.log(b) - 1.0)
    return jnp.where(u <= v, (w - v) - u, (w - u) - v)

