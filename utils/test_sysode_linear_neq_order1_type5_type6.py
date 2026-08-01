
def test_sysode_linear_neq_order1_type5_type6():
    f, g = symbols("f g", cls=Function)
    x, x_ = symbols("x x_")

    # Type 5
    eqs1 = [Eq(Derivative(f(x), x), (2*f(x) + g(x))/x), Eq(Derivative(g(x), x), (f(x) + 2*g(x))/x)]
    sol1 = [Eq(f(x), -C1*x + C2*x**3), Eq(g(x), C1*x + C2*x**3)]
    assert dsolve(eqs1) == sol1
    assert checksysodesol(eqs1, sol1) == (True, [0, 0])

    # Type 6
    eqs2 = [Eq(Derivative(f(x), x), (2*f(x) + g(x) + 1)/x),
            Eq(Derivative(g(x), x), (x + f(x) + 2*g(x))/x)]
    sol2 = [Eq(f(x), C2*x**3 - x*(C1 + Rational(1, 4)) + x*log(x)*Rational(-1, 2) + Rational(-2, 3)),
            Eq(g(x), C2*x**3 + x*log(x)/2 + x*(C1 + Rational(-1, 4)) + Rational(1, 3))]
    assert dsolve(eqs2) == sol2
    assert checksysodesol(eqs2, sol2) == (True, [0, 0])

