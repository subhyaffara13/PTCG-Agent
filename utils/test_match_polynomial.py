
def test_match_polynomial():
    x = Symbol('x')
    a = Wild('a', exclude=[x])
    b = Wild('b', exclude=[x])
    c = Wild('c', exclude=[x])
    d = Wild('d', exclude=[x])

    eq = 4*x**3 + 3*x**2 + 2*x + 1
    pattern = a*x**3 + b*x**2 + c*x + d
    assert eq.match(pattern) == {a: 4, b: 3, c: 2, d: 1}
    assert (eq - 3*x**2).match(pattern) == {a: 4, b: 0, c: 2, d: 1}
    assert (x + sqrt(2) + 3).match(a + b*x + c*x**2) == \
        {b: 1, a: sqrt(2) + 3, c: 0}

