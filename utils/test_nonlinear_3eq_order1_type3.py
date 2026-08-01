
def test_nonlinear_3eq_order1_type3():
    eqs = [
        Eq(f(x).diff(x), (2*f(x)**2 - 3        )),
        Eq(g(x).diff(x), (4         - 2*h(x)   )),
        Eq(h(x).diff(x), (3*h(x)    - 4*f(x)**2)),
    ]
    dsolve(eqs)  # Not sure if this finishes...

