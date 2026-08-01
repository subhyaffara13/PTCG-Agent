
def _fourier_transform(seq, dps, inverse=False):
    """Utility function for the Discrete Fourier Transform"""

    if not iterable(seq):
        raise TypeError("Expected a sequence of numeric coefficients "
                        "for Fourier Transform")

    a = [sympify(arg) for arg in seq]
    if any(x.has(Symbol) for x in a):
        raise ValueError("Expected non-symbolic coefficients")

    n = len(a)
    if n < 2:
        return a

    b = n.bit_length() - 1
    if n&(n - 1): # not a power of 2
        b += 1
        n = 2**b

    a += [S.Zero]*(n - len(a))
    for i in range(1, n):
        j = int(ibin(i, b, str=True)[::-1], 2)
        if i < j:
            a[i], a[j] = a[j], a[i]

    ang = -2*pi/n if inverse else 2*pi/n

    if dps is not None:
        ang = ang.evalf(dps + 2)

    w = [cos(ang*i) + I*sin(ang*i) for i in range(n // 2)]

    h = 2
    while h <= n:
        hf, ut = h // 2, n // h
        for i in range(0, n, h):
            for j in range(hf):
                u, v = a[i + j], expand_mul(a[i + j + hf]*w[ut * j])
                a[i + j], a[i + j + hf] = u + v, u - v
        h *= 2

    if inverse:
        a = [(x/n).evalf(dps) for x in a] if dps is not None \
                            else [x/n for x in a]

    return a


def _fourier_transform(f, x, k, a, b, name, simplify=True):
    r"""
    Compute a general Fourier-type transform

    .. math::

        F(k) = a \int_{-\infty}^{\infty} e^{bixk} f(x)\, dx.

    For suitable choice of *a* and *b*, this reduces to the standard Fourier
    and inverse Fourier transforms.
    """
    F = integrate(a*f*exp(b*S.ImaginaryUnit*x*k), (x, S.NegativeInfinity, S.Infinity))

    if not F.has(Integral):
        return _simplify(F, simplify), S.true

    integral_f = integrate(f, (x, S.NegativeInfinity, S.Infinity))
    if integral_f in (S.NegativeInfinity, S.Infinity, S.NaN) or integral_f.has(Integral):
        raise IntegralTransformError(name, f, 'function not integrable on real axis')

    if not F.is_Piecewise:
        raise IntegralTransformError(name, f, 'could not compute integral')

    F, cond = F.args[0]
    if F.has(Integral):
        raise IntegralTransformError(name, f, 'integral in unexpected form')

    return _simplify(F, simplify), cond

