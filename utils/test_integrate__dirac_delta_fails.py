
def test_integrate_DiracDelta_fails():
    # issue 6427
    # works without meijerg. See test_integrate_DiracDelta_no_meijerg above.
    assert integrate(integrate(integrate(
        DiracDelta(x - y - z), (z, 0, oo)), (y, 0, 1)), (x, 0, 1)) == S.Half

