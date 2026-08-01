
def test_issue_9165():
    z = Symbol('z', zero=True)
    f = Symbol('f', finite=False)
    assert 0/z is S.NaN
    assert 0*(1/z) is S.NaN
    assert 0*f is S.NaN

