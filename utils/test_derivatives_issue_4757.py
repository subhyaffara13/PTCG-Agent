
def test_derivatives_issue_4757():
    x = Symbol('x', real=True)
    y = Symbol('y', imaginary=True)
    f = Function('f')
    assert re(f(x)).diff(x) == re(f(x).diff(x))
    assert im(f(x)).diff(x) == im(f(x).diff(x))
    assert re(f(y)).diff(y) == -I*im(f(y).diff(y))
    assert im(f(y)).diff(y) == -I*re(f(y).diff(y))
    assert Abs(f(x)).diff(x).subs(f(x), 1 + I*x).doit() == x/sqrt(1 + x**2)
    assert arg(f(x)).diff(x).subs(f(x), 1 + I*x**2).doit() == 2*x/(1 + x**4)
    assert Abs(f(y)).diff(y).subs(f(y), 1 + y).doit() == -y/sqrt(1 - y**2)
    assert arg(f(y)).diff(y).subs(f(y), I + y**2).doit() == 2*y/(1 + y**4)

