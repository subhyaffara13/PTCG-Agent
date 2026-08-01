
def _neq_order1_type4_slow3():
    f, g = symbols("f g", cls=Function)
    x = symbols("x")

    eqs = [
        Eq(Derivative(f(x), x), x*f(x) + g(x) + sin(x)),
        Eq(Derivative(g(x), x), x**2 + x*g(x) - f(x))
    ]
    sol = [
        Eq(f(x), (C1/2 - I*C2/2 - I*Integral(x**2*exp(-x**2/2 - I*x)/2 +
            x**2*exp(-x**2/2 + I*x)/2 + I*exp(-x**2/2 - I*x)*sin(x)/2 -
            I*exp(-x**2/2 + I*x)*sin(x)/2, x)/2 + Integral(-I*x**2*exp(-x**2/2
            - I*x)/2 + I*x**2*exp(-x**2/2 + I*x)/2 + exp(-x**2/2 -
            I*x)*sin(x)/2 + exp(-x**2/2 + I*x)*sin(x)/2, x)/2)*exp(x**2/2 +
            I*x) + (C1/2 + I*C2/2 + I*Integral(x**2*exp(-x**2/2 - I*x)/2 +
            x**2*exp(-x**2/2 + I*x)/2 + I*exp(-x**2/2 - I*x)*sin(x)/2 -
            I*exp(-x**2/2 + I*x)*sin(x)/2, x)/2 + Integral(-I*x**2*exp(-x**2/2
            - I*x)/2 + I*x**2*exp(-x**2/2 + I*x)/2 + exp(-x**2/2 -
            I*x)*sin(x)/2 + exp(-x**2/2 + I*x)*sin(x)/2, x)/2)*exp(x**2/2 -
            I*x)),
        Eq(g(x), (-I*C1/2 + C2/2 + Integral(x**2*exp(-x**2/2 - I*x)/2 +
            x**2*exp(-x**2/2 + I*x)/2 + I*exp(-x**2/2 - I*x)*sin(x)/2 -
            I*exp(-x**2/2 + I*x)*sin(x)/2, x)/2 -
            I*Integral(-I*x**2*exp(-x**2/2 - I*x)/2 + I*x**2*exp(-x**2/2 +
            I*x)/2 + exp(-x**2/2 - I*x)*sin(x)/2 + exp(-x**2/2 +
            I*x)*sin(x)/2, x)/2)*exp(x**2/2 - I*x) + (I*C1/2 + C2/2 +
            Integral(x**2*exp(-x**2/2 - I*x)/2 + x**2*exp(-x**2/2 + I*x)/2 +
            I*exp(-x**2/2 - I*x)*sin(x)/2 - I*exp(-x**2/2 + I*x)*sin(x)/2,
            x)/2 + I*Integral(-I*x**2*exp(-x**2/2 - I*x)/2 +
            I*x**2*exp(-x**2/2 + I*x)/2 + exp(-x**2/2 - I*x)*sin(x)/2 +
            exp(-x**2/2 + I*x)*sin(x)/2, x)/2)*exp(x**2/2 + I*x))
    ]

    return eqs, sol

