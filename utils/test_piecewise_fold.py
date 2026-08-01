
def test_piecewise_fold():
    p = Piecewise((x, x < 1), (1, 1 <= x))

    assert piecewise_fold(x*p) == Piecewise((x**2, x < 1), (x, 1 <= x))
    assert piecewise_fold(p + p) == Piecewise((2*x, x < 1), (2, 1 <= x))
    assert piecewise_fold(Piecewise((1, x < 0), (2, True))
                          + Piecewise((10, x < 0), (-10, True))) == \
        Piecewise((11, x < 0), (-8, True))

    p1 = Piecewise((0, x < 0), (x, x <= 1), (0, True))
    p2 = Piecewise((0, x < 0), (1 - x, x <= 1), (0, True))

    p = 4*p1 + 2*p2
    assert integrate(
        piecewise_fold(p), (x, -oo, oo)) == integrate(2*x + 2, (x, 0, 1))

    assert piecewise_fold(
        Piecewise((1, y <= 0), (-Piecewise((2, y >= 0)), True)
        )) == Piecewise((1, y <= 0), (-2, y >= 0))

    assert piecewise_fold(Piecewise((x, ITE(x > 0, y < 1, y > 1)))
        ) == Piecewise((x, ((x <= 0) | (y < 1)) & ((x > 0) | (y > 1))))

    a, b = (Piecewise((2, Eq(x, 0)), (0, True)),
        Piecewise((x, Eq(-x + y, 0)), (1, Eq(-x + y, 1)), (0, True)))
    assert piecewise_fold(Mul(a, b, evaluate=False)
        ) == piecewise_fold(Mul(b, a, evaluate=False))

