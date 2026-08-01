
def test_issue_4700():
    f = Function('f')
    x = Symbol('x')
    a, b = symbols('a b', cls=Wild, exclude=(f(x),))

    p = a*f(x) + b
    eq1 = sin(x)
    eq2 = f(x) + sin(x)
    eq3 = f(x) + x + sin(x)
    eq4 = x + sin(x)

    assert eq1.match(p) == {a: 0, b: sin(x)}
    assert eq2.match(p) == {a: 1, b: sin(x)}
    assert eq3.match(p) == {a: 1, b: x + sin(x)}
    assert eq4.match(p) == {a: 0, b: x + sin(x)}

