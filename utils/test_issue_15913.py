
def test_issue_15913():
    eq = -C1/x - 2*x*f(x) - f(x) + Derivative(f(x), x)
    sol = C2*exp(x**2 + x) + exp(x**2 + x)*Integral(C1*exp(-x**2 - x)/x, x)
    assert checkodesol(eq, sol) == (True, 0)
    sol = C1 + C2*exp(-x*y)
    eq = Derivative(y*f(x), x) + f(x).diff(x, 2)
    assert checkodesol(eq, sol, f(x)) == (True, 0)

