
def test_derivative_subs_bug():
    e = diff(g(x), x)
    assert e.subs(g(x), f(x)) != e
    assert e.subs(g(x), f(x)) == Derivative(f(x), x)
    assert e.subs(g(x), -f(x)) == Derivative(-f(x), x)

    assert e.subs(x, y) == Derivative(g(y), y)

