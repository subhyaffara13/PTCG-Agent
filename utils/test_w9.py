
def test_W9():
    # Integrand with a residue at infinity => -2 pi [sin(pi/5) + sin(2pi/5)]
    # (principal value)   [Levinson and Redheffer, p. 234] *)
    r1 = integrate(5*x**3/(1 + x + x**2 + x**3 + x**4), (x, -oo, oo))
    r2 = r1.doit()
    assert r2 == -2*pi*(sqrt(-sqrt(5)/8 + 5/8) + sqrt(sqrt(5)/8 + 5/8))

