
def test_issue_8657():
    n = Symbol('n', negative=True, integer=True)
    m = Symbol('m', integer=True)
    o = Symbol('o', positive=True)
    p = Symbol('p', negative=True, integer=False)
    assert gamma(n).is_real is False
    assert gamma(m).is_real is None
    assert gamma(o).is_real is True
    assert gamma(p).is_real is True
    assert gamma(w).is_real is None

