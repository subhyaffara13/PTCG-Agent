
def test_deriv1():
    # These all require derivatives evaluated at a point (issue 4719) to work.
    # See issue 4624
    assert f(2*x).diff(x) == 2*Subs(Derivative(f(x), x), x, 2*x)
    assert (f(x)**3).diff(x) == 3*f(x)**2*f(x).diff(x)
    assert (f(2*x)**3).diff(x) == 6*f(2*x)**2*Subs(
        Derivative(f(x), x), x, 2*x)

    assert f(2 + x).diff(x) == Subs(Derivative(f(x), x), x, x + 2)
    assert f(2 + 3*x).diff(x) == 3*Subs(
        Derivative(f(x), x), x, 3*x + 2)
    assert f(3*sin(x)).diff(x) == 3*cos(x)*Subs(
        Derivative(f(x), x), x, 3*sin(x))

    # See issue 8510
    assert f(x, x + z).diff(x) == (
        Subs(Derivative(f(y, x + z), y), y, x) +
        Subs(Derivative(f(x, y), y), y, x + z))
    assert f(x, x**2).diff(x) == (
        2*x*Subs(Derivative(f(x, y), y), y, x**2) +
        Subs(Derivative(f(y, x**2), y), y, x))
    # but Subs is not always necessary
    assert f(x, g(y)).diff(g(y)) == Derivative(f(x, g(y)), g(y))

