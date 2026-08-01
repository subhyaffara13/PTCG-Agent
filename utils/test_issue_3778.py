
def test_issue_3778():
    p, c, q = symbols('p c q', cls=Wild)
    x = Symbol('x')

    assert (sin(x)**2).match(sin(p)*sin(q)*c) == {q: x, c: 1, p: x}
    assert (2*sin(x)).match(sin(p) + sin(q) + c) == {q: x, c: 0, p: x}

