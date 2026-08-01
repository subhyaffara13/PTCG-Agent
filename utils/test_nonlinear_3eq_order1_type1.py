
def test_nonlinear_3eq_order1_type1():
    a, b, c = symbols('a b c')

    eqs = [
        a * f(x).diff(x) - (b - c) * g(x) * h(x),
        b * g(x).diff(x) - (c - a) * h(x) * f(x),
        c * h(x).diff(x) - (a - b) * f(x) * g(x),
    ]

    assert dsolve(eqs) # NotImplementedError

