
def test_Derivative_bug1():
    f = Function("f")
    x = abc.x
    a = Wild("a", exclude=[f(x)])
    b = Wild("b", exclude=[f(x)])
    eq = f(x).diff(x)
    assert eq.match(a*Derivative(f(x), x) + b) == {a: 1, b: 0}

