
def test_issue_5184():
    assert limit(sin(x)/x, x, oo) == 0
    assert limit(atan(x), x, oo) == pi/2
    assert limit(gamma(x), x, oo) is oo
    assert limit(cos(x)/x, x, oo) == 0
    assert limit(gamma(x), x, S.Half) == sqrt(pi)

    r = Symbol('r', real=True)
    assert limit(r*sin(1/r), r, 0) == 0

