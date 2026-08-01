
def test_naturals0():
    N = S.Naturals0
    assert 0 in N
    assert -1 not in N
    assert next(iter(N)) == 0
    assert not N.contains(oo)
    assert N.contains(sin(x)) == Contains(sin(x), N)

