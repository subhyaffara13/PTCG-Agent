
def test_piecewise_exclusive():
    p = Piecewise((0, x < 0), (S.Half, x <= 0), (1, True))
    assert piecewise_exclusive(p) == Piecewise((0, x < 0), (S.Half, Eq(x, 0)),
                                               (1, x > 0), evaluate=False)
    assert piecewise_exclusive(p + 2) == Piecewise((0, x < 0), (S.Half, Eq(x, 0)),
                                               (1, x > 0), evaluate=False) + 2
    assert piecewise_exclusive(Piecewise((1, y <= 0),
                                         (-Piecewise((2, y >= 0)), True))) == \
        Piecewise((1, y <= 0),
                  (-Piecewise((2, y >= 0),
                              (S.NaN, y < 0), evaluate=False), y > 0), evaluate=False)
    assert piecewise_exclusive(Piecewise((1, x > y))) == Piecewise((1, x > y),
                                                                  (S.NaN, x <= y),
                                                                  evaluate=False)
    assert piecewise_exclusive(Piecewise((1, x > y)),
                               skip_nan=True) == Piecewise((1, x > y))

    xr, yr = symbols('xr, yr', real=True)

    p1 = Piecewise((1, xr < 0), (2, True), evaluate=False)
    p1x = Piecewise((1, xr < 0), (2, xr >= 0), evaluate=False)

    p2 = Piecewise((p1, yr < 0), (3, True), evaluate=False)
    p2x = Piecewise((p1, yr < 0), (3, yr >= 0), evaluate=False)
    p2xx = Piecewise((p1x, yr < 0), (3, yr >= 0), evaluate=False)

    assert piecewise_exclusive(p2) == p2xx
    assert piecewise_exclusive(p2, deep=False) == p2x

