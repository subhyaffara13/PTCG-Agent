
def test_piecewise_integrate5_independent_conditions():
    p = Piecewise((0, Eq(y, 0)), (x*y, True))
    assert integrate(p, (x, 1, 3)) == Piecewise((0, Eq(y, 0)), (4*y, True))

