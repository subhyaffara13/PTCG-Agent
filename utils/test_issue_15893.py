
def test_issue_15893():
    f = Function('f', real=True)
    x = Symbol('x', real=True)
    eq = Derivative(Abs(f(x)), f(x))
    assert eq.doit() == sign(f(x))

