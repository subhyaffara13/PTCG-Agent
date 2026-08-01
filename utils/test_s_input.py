
def test_s_input():
    expr = Basic(S(1), S(2))
    a, b = map(Symbol, 'ab')
    pattern = Basic(a, b)
    assert list(unify(expr, pattern, {}, (a, b))) == [{a: 1, b: 2}]
    assert list(unify(expr, pattern, {a: 5}, (a, b))) == []

