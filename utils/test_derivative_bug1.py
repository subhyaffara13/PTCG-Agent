
def test_derivative_bug1():
    f = Function("f")
    x = Symbol("x")
    a = Wild("a", exclude=[f, x])
    b = Wild("b", exclude=[f])
    pattern = a * Derivative(f(x), x, x) + b
    expr = Derivative(f(x), x) + x**2
    d1 = {b: x**2}
    d2 = pattern.xreplace(d1).matches(expr, d1)
    assert d2 is None

