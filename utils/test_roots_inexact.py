
def test_roots_inexact():
    R1 = roots(x**2 + x + 1, x, multiple=True)
    R2 = roots(x**2 + x + 1.0, x, multiple=True)

    for r1, r2 in zip(R1, R2):
        assert abs(r1 - r2) < 1e-12

    f = x**4 + 3.0*sqrt(2.0)*x**3 - (78.0 + 24.0*sqrt(3.0))*x**2 \
        + 144.0*(2*sqrt(3.0) + 9.0)

    R1 = roots(f, multiple=True)
    R2 = (-12.7530479110482, -3.85012393732929,
          4.89897948556636, 7.46155167569183)

    for r1, r2 in zip(R1, R2):
        assert abs(r1 - r2) < 1e-10

