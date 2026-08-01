
def _yn(n, z):
    # (-1)**(n + 1) * _jn(-n - 1, z)
    return (S.NegativeOne**(n + 1) * spherical_bessel_fn(-n - 1, z)*sin(z) -
            spherical_bessel_fn(n, z)*cos(z))

