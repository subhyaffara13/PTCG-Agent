
def test_condition_multiple():
    rl = rewriterule(x + y, x**y, [x,y], lambda x, y: x.is_integer)

    a = Symbol('a')
    b = Symbol('b', integer=True)
    expr = a + b
    assert list(rl(expr)) == [b**a]

    c = Symbol('c', integer=True)
    d = Symbol('d', integer=True)
    assert set(rl(c + d)) == {c**d, d**c}

