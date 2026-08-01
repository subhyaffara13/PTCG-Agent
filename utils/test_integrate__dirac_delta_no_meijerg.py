
def test_integrate_DiracDelta_no_meijerg():
    assert integrate(integrate(integrate(
        DiracDelta(x - y - z), (z, 0, oo)), (y, 0, 1), meijerg=False), (x, 0, 1)) == S.Half

