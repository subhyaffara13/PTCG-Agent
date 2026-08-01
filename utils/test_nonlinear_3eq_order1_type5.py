
def test_nonlinear_3eq_order1_type5():
    eqs = [
        Eq(f(x).diff(x), f(x)*(2*f(x) - 3*g(x))),
        Eq(g(x).diff(x), g(x)*(4*g(x) - 2*h(x))),
        Eq(h(x).diff(x), h(x)*(3*h(x) - 4*f(x))),
    ]
    dsolve(eqs)  # KeyError

