
def test_CRootOf_attributes():
    r = rootof(x**3 + x + 3, 0)
    assert r.is_number
    assert r.free_symbols == set()
    # if the following assertion fails then multivariate polynomials
    # are apparently supported and the RootOf.free_symbols routine
    # should be changed to return whatever symbols would not be
    # the PurePoly dummy symbol
    raises(NotImplementedError, lambda: rootof(Poly(x**3 + y*x + 1, x), 0))

