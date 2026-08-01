
def test_second_order_type2_slow1():
    x, y, z = symbols('x, y, z', cls=Function)
    t, l = symbols('t, l')

    eqs1 = [Eq(Derivative(x(t), (t, 2)), t*(2*x(t) + y(t))),
            Eq(Derivative(y(t), (t, 2)), t*(-x(t) + 2*y(t)))]
    sol1 = [Eq(x(t), I*C1*airyai(t*(2 - I)**(S(1)/3)) + I*C2*airybi(t*(2 - I)**(S(1)/3)) - I*C3*airyai(t*(2 +
             I)**(S(1)/3)) - I*C4*airybi(t*(2 + I)**(S(1)/3))),
            Eq(y(t), C1*airyai(t*(2 - I)**(S(1)/3)) + C2*airybi(t*(2 - I)**(S(1)/3)) + C3*airyai(t*(2 + I)**(S(1)/3)) +
             C4*airybi(t*(2 + I)**(S(1)/3)))]
    assert dsolve(eqs1) == sol1
    assert checksysodesol(eqs1, sol1) == (True, [0, 0])

