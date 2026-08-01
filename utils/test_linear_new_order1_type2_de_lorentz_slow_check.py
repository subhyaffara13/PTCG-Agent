
def test_linear_new_order1_type2_de_lorentz_slow_check():
    m = Symbol("m", real=True)
    q = Symbol("q", real=True)
    t = Symbol("t", real=True)

    e1, e2, e3 = symbols("e1:4", real=True)
    b1, b2, b3 = symbols("b1:4", real=True)
    v1, v2, v3 = symbols("v1:4", cls=Function, real=True)

    eqs = [
        -e1*q + m*Derivative(v1(t), t) - q*(-b2*v3(t) + b3*v2(t)),
        -e2*q + m*Derivative(v2(t), t) - q*(b1*v3(t) - b3*v1(t)),
        -e3*q + m*Derivative(v3(t), t) - q*(-b1*v2(t) + b2*v1(t))
    ]
    sol = dsolve(eqs)
    assert checksysodesol(eqs, sol) == (True, [0, 0, 0])

