
def _complex_sumprod(v1, v2):
    """High precision sumprod() for complex numbers.
    Used by :func:`dft` and :func:`idft`.
    """

    real = attrgetter('real')
    imag = attrgetter('imag')
    r1 = chain(map(real, v1), map(neg, map(imag, v1)))
    r2 = chain(map(real, v2), map(imag, v2))
    i1 = chain(map(real, v1), map(imag, v1))
    i2 = chain(map(imag, v2), map(real, v2))
    return complex(_fsumprod(r1, r2), _fsumprod(i1, i2))

