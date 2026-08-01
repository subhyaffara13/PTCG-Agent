
def test_Poly_terms():
    assert Poly(0, x).terms() == [((0,), 0)]
    assert Poly(1, x).terms() == [((0,), 1)]

    assert Poly(2*x + 1, x).terms() == [((1,), 2), ((0,), 1)]

    assert Poly(7*x**2 + 2*x + 1, x).terms() == [((2,), 7), ((1,), 2), ((0,), 1)]
    assert Poly(7*x**4 + 2*x + 1, x).terms() == [((4,), 7), ((1,), 2), ((0,), 1)]

    assert Poly(
        x*y**7 + 2*x**2*y**3).terms('lex') == [((2, 3), 2), ((1, 7), 1)]
    assert Poly(
        x*y**7 + 2*x**2*y**3).terms('grlex') == [((1, 7), 1), ((2, 3), 2)]

