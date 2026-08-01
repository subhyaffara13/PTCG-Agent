
def test_piecewise_integrate1cb():
    y = symbols('y', real=True)
    g = Piecewise(
        (0, Or(x <= -1, x >= 1)),
        (1 - x, x > 0),
        (1 + x, True)
        )
    gy1 = g.integrate((x, y, 1))
    g1y = g.integrate((x, 1, y))

    assert g.integrate((x, -2, 1)) == gy1.subs(y, -2)
    assert g.integrate((x, 1, -2)) == g1y.subs(y, -2)
    assert g.integrate((x, 0, 1)) == gy1.subs(y, 0)
    assert g.integrate((x, 1, 0)) == g1y.subs(y, 0)
    assert g.integrate((x, 2, 1)) == gy1.subs(y, 2)
    assert g.integrate((x, 1, 2)) == g1y.subs(y, 2)

    assert piecewise_fold(gy1.rewrite(Piecewise)
        ).simplify() == Piecewise(
            (1, y <= -1),
            (-y**2/2 - y + S.Half, y <= 0),
            (y**2/2 - y + S.Half, y < 1),
            (0, True))
    assert piecewise_fold(g1y.rewrite(Piecewise)
        ).simplify() == Piecewise(
            (-1, y <= -1),
            (y**2/2 + y - S.Half, y <= 0),
            (-y**2/2 + y - S.Half, y < 1),
            (0, True))

    # g1y and gy1 should simplify if the condition that y < 1
    # is applied, e.g. Min(1, Max(-1, y)) --> Max(-1, y)
    assert gy1 == Piecewise(
        (
            -Min(1, Max(-1, y))**2/2 - Min(1, Max(-1, y)) +
            Min(1, Max(0, y))**2 + S.Half, y < 1),
        (0, True)
        )
    assert g1y == Piecewise(
        (
            Min(1, Max(-1, y))**2/2 + Min(1, Max(-1, y)) -
            Min(1, Max(0, y))**2 - S.Half, y < 1),
        (0, True))

