
def test_unify():
    expr = Basic(S(1), S(2), S(3))
    a, b, c = map(Symbol, 'abc')
    pattern = Basic(a, b, c)
    assert list(unify(expr, pattern, {}, (a, b, c))) == [{a: 1, b: 2, c: 3}]
    assert list(unify(expr, pattern, variables=(a, b, c))) == \
            [{a: 1, b: 2, c: 3}]

