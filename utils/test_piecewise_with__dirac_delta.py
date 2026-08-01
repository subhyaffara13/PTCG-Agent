
def test_piecewise_with_DiracDelta():
    d1 = DiracDelta(x - 1)
    assert integrate(d1, (x, -oo, oo)) == 1
    assert integrate(d1, (x, 0, 2)) == 1
    assert Piecewise((d1, Eq(x, 2)), (0, True)).integrate(x) == 0
    assert Piecewise((d1, x < 2), (0, True)).integrate(x) == Piecewise(
        (Heaviside(x - 1), x < 2), (1, True))

