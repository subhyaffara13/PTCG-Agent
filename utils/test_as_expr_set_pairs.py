
def test_as_expr_set_pairs():
    assert Piecewise((x, x > 0), (-x, x <= 0)).as_expr_set_pairs() == \
        [(x, Interval(0, oo, True, True)), (-x, Interval(-oo, 0))]

    assert Piecewise(((x - 2)**2, x >= 0), (0, True)).as_expr_set_pairs() == \
        [((x - 2)**2, Interval(0, oo)), (0, Interval(-oo, 0, True, True))]

