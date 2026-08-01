
def test_exponentiation():
    f = lambdify(x, x**2)
    assert f(-1) == 1
    assert f(0) == 0
    assert f(1) == 1
    assert f(-2) == 4
    assert f(2) == 4
    assert f(2.5) == 6.25


def test_exponentiation():
    w = omega
    assert w**2 == w*w
    assert w**3 == w*w*w
    assert w**(w + 1) == Ordinal(OmegaPower(omega + 1, 1))
    assert (w**w)*(w**w) == w**(w*2)

