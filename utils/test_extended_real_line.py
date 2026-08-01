
def test_extended_real_line():
    assert limit(x - oo, x, oo) == Limit(x - oo, x, oo)
    assert limit(1/(x + sin(x)) - oo, x, 0) == Limit(1/(x + sin(x)) - oo, x, 0)
    assert limit(oo/x, x, oo) == Limit(oo/x, x, oo)
    assert limit(x - oo + 1/x, x, oo) == Limit(x - oo + 1/x, x, oo)

