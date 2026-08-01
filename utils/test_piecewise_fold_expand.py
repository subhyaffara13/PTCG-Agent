
def test_piecewise_fold_expand():
    p1 = Piecewise((1, Interval(0, 1, False, True).contains(x)), (0, True))

    p2 = piecewise_fold(expand((1 - x)*p1))
    cond = ((x >= 0) & (x < 1))
    assert piecewise_fold(expand((1 - x)*p1), evaluate=False
        ) == Piecewise((1 - x, cond), (-x, cond), (1, cond), (0, True), evaluate=False)
    assert piecewise_fold(expand((1 - x)*p1), evaluate=None
        ) == Piecewise((1 - x, cond), (0, True))
    assert p2 == Piecewise((1 - x, cond), (0, True))
    assert p2 == expand(piecewise_fold((1 - x)*p1))

