
def test_solve_poly_inequality():
    assert psolve(Poly(0, x), '==') == [S.Reals]
    assert psolve(Poly(1, x), '==') == [S.EmptySet]
    assert psolve(PurePoly(x + 1, x), ">") == [Interval(-1, oo, True, False)]

