
def test_L9():
    z = symbols('z', complex=True)
    assert simplify(2**(1 - z)*gamma(z)*zeta(z)*cos(z*pi/2) - pi**2*zeta(1 - z)) == 0

