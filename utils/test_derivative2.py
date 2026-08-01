
def test_derivative2():
    f = Function("f")
    x = Symbol("x")
    a = Wild("a", exclude=[f, x])
    b = Wild("b", exclude=[f])
    e = Derivative(f(x), x)
    assert e.match(Derivative(f(x), x)) == {}
    assert e.match(Derivative(f(x), x, x)) is None
    e = Derivative(f(x), x, x)
    assert e.match(Derivative(f(x), x)) is None
    assert e.match(Derivative(f(x), x, x)) == {}
    e = Derivative(f(x), x) + x**2
    assert e.match(a*Derivative(f(x), x) + b) == {a: 1, b: x**2}
    assert e.match(a*Derivative(f(x), x, x) + b) is None
    e = Derivative(f(x), x, x) + x**2
    assert e.match(a*Derivative(f(x), x) + b) is None
    assert e.match(a*Derivative(f(x), x, x) + b) == {a: 1, b: x**2}

