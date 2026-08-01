
def test_derivative_subs():
    f = Function('f')
    g = Function('g')
    assert Derivative(f(x), x).subs(f(x), y) != 0
    # need xreplace to put the function back, see #13803
    assert Derivative(f(x), x).subs(f(x), y).xreplace({y: f(x)}) == \
        Derivative(f(x), x)
    # issues 5085, 5037
    assert cse(Derivative(f(x), x) + f(x))[1][0].has(Derivative)
    assert cse(Derivative(f(x, y), x) +
               Derivative(f(x, y), y))[1][0].has(Derivative)
    eq = Derivative(g(x), g(x))
    assert eq.subs(g, f) == Derivative(f(x), f(x))
    assert eq.subs(g(x), f(x)) == Derivative(f(x), f(x))
    assert eq.subs(g, cos) == Subs(Derivative(y, y), y, cos(x))

