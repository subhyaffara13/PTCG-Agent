
def test_piecewise_duplicate():
    p = Piecewise((x, x < -10), (x**2, x <= -1), (x, 1 < x))
    assert p == Piecewise(*p.args)

