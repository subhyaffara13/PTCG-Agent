
def test_energy(n=1):
    # Maximum "n" which is tested:
    for i in range(n+1):
        assert simplify(
            energy(i, m, r) - ((i**2 * hbar**2) / (2 * m * r**2))) == 0


def test_energy():
    n, l, hw = symbols('n l hw')
    assert simplify(E_nl(n, l, hw) - (2*n + l + Rational(3, 2))*hw) == 0

