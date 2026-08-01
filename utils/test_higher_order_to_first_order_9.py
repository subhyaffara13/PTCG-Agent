
def test_higher_order_to_first_order_9():
    f, g = symbols('f g', cls=Function)
    x = symbols('x')

    eqs9 = [f(x) + g(x) - 2*exp(I*x) + 2*Derivative(f(x), x) + Derivative(f(x), (x, 2)),
            f(x) + g(x) - 2*exp(I*x) + 2*Derivative(g(x), x) + Derivative(g(x), (x, 2))]
    sol9 =  [Eq(f(x), -C1 + C4*exp(-2*x)/2 - (C2/2 - C3/2)*exp(-x)*cos(x)
                    + (C2/2 + C3/2)*exp(-x)*sin(x) + 2*((1 - 2*I)*exp(I*x)*sin(x)**2/5)
                    + 2*((1 - 2*I)*exp(I*x)*cos(x)**2/5)),
            Eq(g(x), C1 - C4*exp(-2*x)/2 - (C2/2 - C3/2)*exp(-x)*cos(x)
                    + (C2/2 + C3/2)*exp(-x)*sin(x) + 2*((1 - 2*I)*exp(I*x)*sin(x)**2/5)
                    + 2*((1 - 2*I)*exp(I*x)*cos(x)**2/5))]
    assert dsolve(eqs9) == sol9
    assert checksysodesol(eqs9, sol9) == (True, [0, 0])

