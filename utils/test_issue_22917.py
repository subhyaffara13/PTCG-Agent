
def test_issue_22917():
    p = (Piecewise((0, ITE((x - y > 1) | (2 * x - 2 * y > 1), False,
                           ITE(x - y > 1, 2 * y - 2 < -1, 2 * x - 2 * y > 1))),
                   (Piecewise((0, ITE(x - y > 1, True, 2 * x - 2 * y > 1)),
                              (2 * Piecewise((0, x - y > 1), (y, True)), True)), True))
         + 2 * Piecewise((1, ITE((x - y > 1) | (2 * x - 2 * y > 1), False,
                                 ITE(x - y > 1, 2 * y - 2 < -1, 2 * x - 2 * y > 1))),
                         (Piecewise((1, ITE(x - y > 1, True, 2 * x - 2 * y > 1)),
                                    (2 * Piecewise((1, x - y > 1), (x, True)), True)), True)))
    assert piecewise_fold(p) == Piecewise((2, (x - y > S.Half) | (x - y > 1)),
                                          (2*y + 4, x - y > 1),
                                          (4*x + 2*y, True))
    assert piecewise_fold(p > 1).rewrite(ITE) == ITE((x - y > S.Half) | (x - y > 1), True,
                                                     ITE(x - y > 1, 2*y + 4 > 1, 4*x + 2*y > 1))

