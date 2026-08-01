
def test_higher_order_to_first_order_12():
    f, g = symbols('f g', cls=Function)
    x = symbols('x')

    x, y = symbols('x, y', cls=Function)
    t, l = symbols('t, l')

    eqs12 = [Eq(4*x(t) + Derivative(x(t), (t, 2)) + 8*Derivative(y(t), t), 0),
             Eq(4*y(t) - 8*Derivative(x(t), t) + Derivative(y(t), (t, 2)), 0)]
    sol12 = [Eq(y(t), C1*(2 - sqrt(5))*sin(2*t*sqrt(4*sqrt(5) + 9))*Rational(-1, 2) + C2*(2 -
              sqrt(5))*cos(2*t*sqrt(4*sqrt(5) + 9))/2 + C3*(2 + sqrt(5))*sin(2*t*sqrt(9 - 4*sqrt(5)))*Rational(-1,
              2) + C4*(2 + sqrt(5))*cos(2*t*sqrt(9 - 4*sqrt(5)))/2),
             Eq(x(t), C1*(2 - sqrt(5))*cos(2*t*sqrt(4*sqrt(5) + 9))*Rational(-1, 2) + C2*(2 -
              sqrt(5))*sin(2*t*sqrt(4*sqrt(5) + 9))*Rational(-1, 2) + C3*(2 + sqrt(5))*cos(2*t*sqrt(9 -
              4*sqrt(5)))/2 + C4*(2 + sqrt(5))*sin(2*t*sqrt(9 - 4*sqrt(5)))/2)]
    assert dsolve(eqs12) == sol12
    assert checksysodesol(eqs12, sol12) == (True, [0, 0])

