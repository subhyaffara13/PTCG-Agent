
def test_issue_19770():
    m = Symbol('m')
    # the result is not 0 for non-real m
    assert limit(cos(m*x)/x, x, oo) == Limit(cos(m*x)/x, x, oo, dir='-')
    m = Symbol('m', real=True)
    # can be improved to give the correct result 0
    assert limit(cos(m*x)/x, x, oo) == Limit(cos(m*x)/x, x, oo, dir='-')
    m = Symbol('m', nonzero=True)
    assert limit(cos(m*x), x, oo) == AccumBounds(-1, 1)
    assert limit(cos(m*x)/x, x, oo) == 0

