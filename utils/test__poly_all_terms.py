
def test_Poly_all_terms():
    assert Poly(0, x).all_terms() == [((0,), 0)]
    assert Poly(1, x).all_terms() == [((0,), 1)]

    assert Poly(2*x + 1, x).all_terms() == [((1,), 2), ((0,), 1)]

    assert Poly(7*x**2 + 2*x + 1, x).all_terms() == \
        [((2,), 7), ((1,), 2), ((0,), 1)]
    assert Poly(7*x**4 + 2*x + 1, x).all_terms() == \
        [((4,), 7), ((3,), 0), ((2,), 0), ((1,), 2), ((0,), 1)]

