
def test_nonlinear_3eq_order1_type4():
    eqs = [
        Eq(f(x).diff(x), (2*h(x)*g(x) - 3*g(x)*h(x))),
        Eq(g(x).diff(x), (4*f(x)*h(x) - 2*h(x)*f(x))),
        Eq(h(x).diff(x), (3*g(x)*f(x) - 4*f(x)*g(x))),
    ]
    dsolve(eqs)  # KeyError when matching

