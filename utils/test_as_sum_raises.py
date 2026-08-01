
def test_as_sum_raises():
    e = Integral((x + y)**2, (x, 0, 1))
    raises(ValueError, lambda: e.as_sum(-1))
    raises(ValueError, lambda: e.as_sum(0))
    raises(ValueError, lambda: Integral(x).as_sum(3))
    raises(ValueError, lambda: e.as_sum(oo))
    raises(ValueError, lambda: e.as_sum(3, method='xxxx2'))

