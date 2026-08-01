
def test_newton():
    R, x = ring('x', QQ)
    p = x**2 - 2
    r = rs_newton(p, x, 4)
    assert r == 8*x**4 + 4*x**2 + 2

