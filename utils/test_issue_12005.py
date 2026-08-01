
def test_issue_12005():
    e1 = Subs(Derivative(f(x), x), x, x)
    assert e1.diff(x) == Derivative(f(x), x, x)
    e2 = Subs(Derivative(f(x), x), x, x**2 + 1)
    assert e2.diff(x) == 2*x*Subs(Derivative(f(x), x, x), x, x**2 + 1)
    e3 = Subs(Derivative(f(x) + y**2 - y, y), y, y**2)
    assert e3.diff(y) == 4*y
    e4 = Subs(Derivative(f(x + y), y), y, (x**2))
    assert e4.diff(y) is S.Zero
    e5 = Subs(Derivative(f(x), x), (y, z), (y, z))
    assert e5.diff(x) == Derivative(f(x), x, x)
    assert f(g(x)).diff(g(x), g(x)) == Derivative(f(g(x)), g(x), g(x))

