
def test_issue_4418():
    x = Symbol('x')
    a, b, c = symbols('a b c', cls=Wild, exclude=(x,))
    f, g = symbols('f g', cls=Function)

    eq = diff(g(x)*f(x).diff(x), x)

    assert eq.match(
        g(x).diff(x)*f(x).diff(x) + g(x)*f(x).diff(x, x) + c) == {c: 0}
    assert eq.match(a*g(x).diff(
        x)*f(x).diff(x) + b*g(x)*f(x).diff(x, x) + c) == {a: 1, b: 1, c: 0}

