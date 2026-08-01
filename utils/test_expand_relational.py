
def test_expand_relational():
    n = symbols('n', negative=True)
    p, q = symbols('p q', positive=True)
    r = ((n + q * (-n / q + 1)) / (q * (-n / q + 1)) < 0)
    assert r is not S.false
    assert r.expand() is S.false
    assert (q > 0).expand() is S.true

