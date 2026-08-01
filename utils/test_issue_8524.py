
def test_issue_8524():
    x = Symbol('x', positive=True)
    y = Symbol('y', negative=True)
    z = Symbol('z', positive=False)
    p = Symbol('p', negative=False)
    q = Symbol('q', integer=True)
    r = Symbol('r', integer=False)
    e = Symbol('e', even=True, negative=True)
    assert gamma(x).is_positive is True
    assert gamma(y).is_positive is None
    assert gamma(z).is_positive is None
    assert gamma(p).is_positive is None
    assert gamma(q).is_positive is None
    assert gamma(r).is_positive is None
    assert gamma(e + S.Half).is_positive is True
    assert gamma(e - S.Half).is_positive is False

