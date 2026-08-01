
def test_sysode_linear_neq_order1_type1_slow():

    t = Symbol('t')
    Z0 = Function('Z0')
    Z1 = Function('Z1')
    Z2 = Function('Z2')
    Z3 = Function('Z3')

    k01, k10, k20, k21, k23, k30 = symbols('k01 k10 k20 k21 k23 k30')

    eqs1 = [Eq(Derivative(Z0(t), t), -k01*Z0(t) + k10*Z1(t) + k20*Z2(t) + k30*Z3(t)),
            Eq(Derivative(Z1(t), t), k01*Z0(t) - k10*Z1(t) + k21*Z2(t)),
            Eq(Derivative(Z2(t), t), (-k20 - k21 - k23)*Z2(t)),
            Eq(Derivative(Z3(t), t), k23*Z2(t) - k30*Z3(t))]
    sol1 = [Eq(Z0(t), C1*k10/k01 - C2*(k10 - k30)*exp(-k30*t)/(k01 + k10 - k30) - C3*(k10*(k20 + k21 - k30) -
             k20**2 - k20*(k21 + k23 - k30) + k23*k30)*exp(-t*(k20 + k21 + k23))/(k23*(-k01 - k10 + k20 + k21 +
             k23)) - C4*exp(-t*(k01 + k10))),
            Eq(Z1(t), C1 - C2*k01*exp(-k30*t)/(k01 + k10 - k30) + C3*(-k01*(k20 + k21 - k30) + k20*k21 + k21**2
             + k21*(k23 - k30))*exp(-t*(k20 + k21 + k23))/(k23*(-k01 - k10 + k20 + k21 + k23)) + C4*exp(-t*(k01 +
             k10))),
            Eq(Z2(t), -C3*(k20 + k21 + k23 - k30)*exp(-t*(k20 + k21 + k23))/k23),
            Eq(Z3(t), C2*exp(-k30*t) + C3*exp(-t*(k20 + k21 + k23)))]
    assert dsolve(eqs1) == sol1
    assert checksysodesol(eqs1, sol1) == (True, [0, 0, 0, 0])

    x, y, z, u, v, w = symbols('x y z u v w', cls=Function)
    k2, k3 = symbols('k2 k3')
    a_b, a_c = symbols('a_b a_c', real=True)

    eqs2 = [Eq(Derivative(z(t), t), k2*y(t)),
            Eq(Derivative(x(t), t), k3*y(t)),
            Eq(Derivative(y(t), t), (-k2 - k3)*y(t))]
    sol2 = [Eq(z(t), C1 - C2*k2*exp(-t*(k2 + k3))/(k2 + k3)),
            Eq(x(t), -C2*k3*exp(-t*(k2 + k3))/(k2 + k3) + C3),
            Eq(y(t), C2*exp(-t*(k2 + k3)))]
    assert dsolve(eqs2) == sol2
    assert checksysodesol(eqs2, sol2) == (True, [0, 0, 0])

    eqs3 = [4*u(t) - v(t) - 2*w(t) + Derivative(u(t), t),
            2*u(t) + v(t) - 2*w(t) + Derivative(v(t), t),
            5*u(t) + v(t) - 3*w(t) + Derivative(w(t), t)]
    sol3 = [Eq(u(t), C3*exp(-2*t) + (C1/2 + sqrt(3)*C2/6)*cos(sqrt(3)*t) + sin(sqrt(3)*t)*(sqrt(3)*C1/6 +
             C2*Rational(-1, 2))),
            Eq(v(t), (C1/2 + sqrt(3)*C2/6)*cos(sqrt(3)*t) + sin(sqrt(3)*t)*(sqrt(3)*C1/6 + C2*Rational(-1, 2))),
            Eq(w(t), C1*cos(sqrt(3)*t) - C2*sin(sqrt(3)*t) + C3*exp(-2*t))]
    assert dsolve(eqs3) == sol3
    assert checksysodesol(eqs3, sol3) == (True, [0, 0, 0])

    eqs4 = [Eq(Derivative(x(t), t), w(t)*Rational(-2, 9) + 2*x(t) + y(t) + z(t)*Rational(-8, 9)),
            Eq(Derivative(y(t), t), w(t)*Rational(4, 9) + 2*y(t) + z(t)*Rational(16, 9)),
            Eq(Derivative(z(t), t), w(t)*Rational(-2, 9) + z(t)*Rational(37, 9)),
            Eq(Derivative(w(t), t), w(t)*Rational(44, 9) + z(t)*Rational(-4, 9))]
    sol4 = [Eq(x(t), C1*exp(2*t) + C2*t*exp(2*t)),
            Eq(y(t), C2*exp(2*t) + 2*C3*exp(4*t)),
            Eq(z(t), 2*C3*exp(4*t) + C4*exp(5*t)*Rational(-1, 4)),
            Eq(w(t), C3*exp(4*t) + C4*exp(5*t))]
    assert dsolve(eqs4) == sol4
    assert checksysodesol(eqs4, sol4) == (True, [0, 0, 0, 0])

    # Regression test case for issue #15574
    # https://github.com/sympy/sympy/issues/15574
    eq5 = [Eq(x(t).diff(t), x(t)), Eq(y(t).diff(t), y(t)), Eq(z(t).diff(t), z(t)), Eq(w(t).diff(t), w(t))]
    sol5 = [Eq(x(t), C1*exp(t)), Eq(y(t), C2*exp(t)), Eq(z(t), C3*exp(t)), Eq(w(t), C4*exp(t))]
    assert dsolve(eq5) == sol5
    assert checksysodesol(eq5, sol5) == (True, [0, 0, 0, 0])

    eqs6 = [Eq(Derivative(x(t), t), x(t) + y(t)),
            Eq(Derivative(y(t), t), y(t) + z(t)),
            Eq(Derivative(z(t), t), w(t)*Rational(-1, 8) + z(t)),
            Eq(Derivative(w(t), t), w(t)/2 + z(t)/2)]
    sol6 = [Eq(x(t), C1*exp(t) + C2*t*exp(t) + 4*C4*t*exp(t*Rational(3, 4)) + (4*C3 + 48*C4)*exp(t*Rational(3,
             4))),
            Eq(y(t), C2*exp(t) - C4*t*exp(t*Rational(3, 4)) - (C3 + 8*C4)*exp(t*Rational(3, 4))),
            Eq(z(t), C4*t*exp(t*Rational(3, 4))/4 + (C3/4 + C4)*exp(t*Rational(3, 4))),
            Eq(w(t), C3*exp(t*Rational(3, 4))/2 + C4*t*exp(t*Rational(3, 4))/2)]
    assert dsolve(eqs6) == sol6
    assert checksysodesol(eqs6, sol6) == (True, [0, 0, 0, 0])

    # Regression test case for issue #15574
    # https://github.com/sympy/sympy/issues/15574
    eq7 = [Eq(Derivative(x(t), t), x(t)), Eq(Derivative(y(t), t), y(t)), Eq(Derivative(z(t), t), z(t)),
           Eq(Derivative(w(t), t), w(t)), Eq(Derivative(u(t), t), u(t))]
    sol7 = [Eq(x(t), C1*exp(t)), Eq(y(t), C2*exp(t)), Eq(z(t), C3*exp(t)), Eq(w(t), C4*exp(t)),
            Eq(u(t), C5*exp(t))]
    assert dsolve(eq7) == sol7
    assert checksysodesol(eq7, sol7) == (True, [0, 0, 0, 0, 0])

    eqs8 = [Eq(Derivative(x(t), t), 2*x(t) + y(t)),
            Eq(Derivative(y(t), t), 2*y(t)),
            Eq(Derivative(z(t), t), 4*z(t)),
            Eq(Derivative(w(t), t), u(t) + 5*w(t)),
            Eq(Derivative(u(t), t), 5*u(t))]
    sol8 = [Eq(x(t), C1*exp(2*t) + C2*t*exp(2*t)),
            Eq(y(t), C2*exp(2*t)),
            Eq(z(t), C3*exp(4*t)),
            Eq(w(t), C4*exp(5*t) + C5*t*exp(5*t)),
            Eq(u(t), C5*exp(5*t))]
    assert dsolve(eqs8) == sol8
    assert checksysodesol(eqs8, sol8) == (True, [0, 0, 0, 0, 0])

    # Regression test case for issue #15574
    # https://github.com/sympy/sympy/issues/15574
    eq9 = [Eq(Derivative(x(t), t), x(t)), Eq(Derivative(y(t), t), y(t)), Eq(Derivative(z(t), t), z(t))]
    sol9 = [Eq(x(t), C1*exp(t)), Eq(y(t), C2*exp(t)), Eq(z(t), C3*exp(t))]
    assert dsolve(eq9) == sol9
    assert checksysodesol(eq9, sol9) == (True, [0, 0, 0])

    # Regression test case for issue #15407
    # https://github.com/sympy/sympy/issues/15407
    eqs10 = [Eq(Derivative(x(t), t), (-a_b - a_c)*x(t)),
             Eq(Derivative(y(t), t), a_b*y(t)),
             Eq(Derivative(z(t), t), a_c*x(t))]
    sol10 = [Eq(x(t), -C1*(a_b + a_c)*exp(-t*(a_b + a_c))/a_c),
             Eq(y(t), C2*exp(a_b*t)),
             Eq(z(t), C1*exp(-t*(a_b + a_c)) + C3)]
    assert dsolve(eqs10) == sol10
    assert checksysodesol(eqs10, sol10) == (True, [0, 0, 0])

    # Regression test case for issue #14312
    # https://github.com/sympy/sympy/issues/14312
    eqs11 = [Eq(Derivative(x(t), t), k3*y(t)),
             Eq(Derivative(y(t), t), (-k2 - k3)*y(t)),
             Eq(Derivative(z(t), t), k2*y(t))]
    sol11 = [Eq(x(t), C1 + C2*k3*exp(-t*(k2 + k3))/k2),
             Eq(y(t), -C2*(k2 + k3)*exp(-t*(k2 + k3))/k2),
             Eq(z(t), C2*exp(-t*(k2 + k3)) + C3)]
    assert dsolve(eqs11) == sol11
    assert checksysodesol(eqs11, sol11) == (True, [0, 0, 0])

    # Regression test case for issue #14312
    # https://github.com/sympy/sympy/issues/14312
    eqs12 = [Eq(Derivative(z(t), t), k2*y(t)),
             Eq(Derivative(x(t), t), k3*y(t)),
             Eq(Derivative(y(t), t), (-k2 - k3)*y(t))]
    sol12 = [Eq(z(t), C1 - C2*k2*exp(-t*(k2 + k3))/(k2 + k3)),
             Eq(x(t), -C2*k3*exp(-t*(k2 + k3))/(k2 + k3) + C3),
             Eq(y(t), C2*exp(-t*(k2 + k3)))]
    assert dsolve(eqs12) == sol12
    assert checksysodesol(eqs12, sol12) == (True, [0, 0, 0])

    f, g, h = symbols('f, g, h', cls=Function)
    a, b, c = symbols('a, b, c')

    # Regression test case for issue #15474
    # https://github.com/sympy/sympy/issues/15474
    eqs13 = [Eq(Derivative(f(t), t), 2*f(t) + g(t)),
             Eq(Derivative(g(t), t), a*f(t))]
    sol13 = [Eq(f(t), C1*exp(t*(sqrt(a + 1) + 1))/(sqrt(a + 1) - 1) - C2*exp(-t*(sqrt(a + 1) - 1))/(sqrt(a + 1) +
              1)),
             Eq(g(t), C1*exp(t*(sqrt(a + 1) + 1)) + C2*exp(-t*(sqrt(a + 1) - 1)))]
    assert dsolve(eqs13) == sol13
    assert checksysodesol(eqs13, sol13) == (True, [0, 0])

    eqs14 = [Eq(Derivative(f(t), t), 2*g(t) - 3*h(t)),
             Eq(Derivative(g(t), t), -2*f(t) + 4*h(t)),
             Eq(Derivative(h(t), t), 3*f(t) - 4*g(t))]
    sol14 = [Eq(f(t), 2*C1 - sin(sqrt(29)*t)*(sqrt(29)*C2*Rational(3, 25) + C3*Rational(-8, 25)) -
              cos(sqrt(29)*t)*(C2*Rational(8, 25) + sqrt(29)*C3*Rational(3, 25))),
             Eq(g(t), C1*Rational(3, 2) + sin(sqrt(29)*t)*(sqrt(29)*C2*Rational(4, 25) + C3*Rational(6, 25)) -
              cos(sqrt(29)*t)*(C2*Rational(6, 25) + sqrt(29)*C3*Rational(-4, 25))),
             Eq(h(t), C1 + C2*cos(sqrt(29)*t) - C3*sin(sqrt(29)*t))]
    assert dsolve(eqs14) == sol14
    assert checksysodesol(eqs14, sol14) == (True, [0, 0, 0])

    eqs15 = [Eq(2*Derivative(f(t), t), 12*g(t) - 12*h(t)),
             Eq(3*Derivative(g(t), t), -8*f(t) + 8*h(t)),
             Eq(4*Derivative(h(t), t), 6*f(t) - 6*g(t))]
    sol15 = [Eq(f(t), C1 - sin(sqrt(29)*t)*(sqrt(29)*C2*Rational(6, 13) + C3*Rational(-16, 13)) -
              cos(sqrt(29)*t)*(C2*Rational(16, 13) + sqrt(29)*C3*Rational(6, 13))),
             Eq(g(t), C1 + sin(sqrt(29)*t)*(sqrt(29)*C2*Rational(8, 39) + C3*Rational(16, 13)) -
              cos(sqrt(29)*t)*(C2*Rational(16, 13) + sqrt(29)*C3*Rational(-8, 39))),
             Eq(h(t), C1 + C2*cos(sqrt(29)*t) - C3*sin(sqrt(29)*t))]
    assert dsolve(eqs15) == sol15
    assert checksysodesol(eqs15, sol15) == (True, [0, 0, 0])

    eq16 = (Eq(diff(x(t), t), 21*x(t)), Eq(diff(y(t), t), 17*x(t) + 3*y(t)),
            Eq(diff(z(t), t), 5*x(t) + 7*y(t) + 9*z(t)))
    sol16 = [Eq(x(t), 216*C1*exp(21*t)/209),
             Eq(y(t), 204*C1*exp(21*t)/209 - 6*C2*exp(3*t)/7),
             Eq(z(t), C1*exp(21*t) + C2*exp(3*t) + C3*exp(9*t))]
    assert dsolve(eq16) == sol16
    assert checksysodesol(eq16, sol16) == (True, [0, 0, 0])

    eqs17 = [Eq(Derivative(x(t), t), 3*y(t) - 11*z(t)),
             Eq(Derivative(y(t), t), -3*x(t) + 7*z(t)),
             Eq(Derivative(z(t), t), 11*x(t) - 7*y(t))]
    sol17 = [Eq(x(t), C1*Rational(7, 3) - sin(sqrt(179)*t)*(sqrt(179)*C2*Rational(11, 170) + C3*Rational(-21,
              170)) - cos(sqrt(179)*t)*(C2*Rational(21, 170) + sqrt(179)*C3*Rational(11, 170))),
             Eq(y(t), C1*Rational(11, 3) + sin(sqrt(179)*t)*(sqrt(179)*C2*Rational(7, 170) + C3*Rational(33,
              170)) - cos(sqrt(179)*t)*(C2*Rational(33, 170) + sqrt(179)*C3*Rational(-7, 170))),
             Eq(z(t), C1 + C2*cos(sqrt(179)*t) - C3*sin(sqrt(179)*t))]
    assert dsolve(eqs17) == sol17
    assert checksysodesol(eqs17, sol17) == (True, [0, 0, 0])

    eqs18 = [Eq(3*Derivative(x(t), t), 20*y(t) - 20*z(t)),
             Eq(4*Derivative(y(t), t), -15*x(t) + 15*z(t)),
             Eq(5*Derivative(z(t), t), 12*x(t) - 12*y(t))]
    sol18 = [Eq(x(t), C1 - sin(5*sqrt(2)*t)*(sqrt(2)*C2*Rational(4, 3) - C3) - cos(5*sqrt(2)*t)*(C2 +
              sqrt(2)*C3*Rational(4, 3))),
             Eq(y(t), C1 + sin(5*sqrt(2)*t)*(sqrt(2)*C2*Rational(3, 4) + C3) - cos(5*sqrt(2)*t)*(C2 +
              sqrt(2)*C3*Rational(-3, 4))),
             Eq(z(t), C1 + C2*cos(5*sqrt(2)*t) - C3*sin(5*sqrt(2)*t))]
    assert dsolve(eqs18) == sol18
    assert checksysodesol(eqs18, sol18) == (True, [0, 0, 0])

    eqs19 = [Eq(Derivative(x(t), t), 4*x(t) - z(t)),
             Eq(Derivative(y(t), t), 2*x(t) + 2*y(t) - z(t)),
             Eq(Derivative(z(t), t), 3*x(t) + y(t))]
    sol19 = [Eq(x(t), C2*t**2*exp(2*t)/2 + t*(2*C2 + C3)*exp(2*t) + (C1 + C2 + 2*C3)*exp(2*t)),
             Eq(y(t), C2*t**2*exp(2*t)/2 + t*(2*C2 + C3)*exp(2*t) + (C1 + 2*C3)*exp(2*t)),
             Eq(z(t), C2*t**2*exp(2*t) + t*(3*C2 + 2*C3)*exp(2*t) + (2*C1 + 3*C3)*exp(2*t))]
    assert dsolve(eqs19) == sol19
    assert checksysodesol(eqs19, sol19) == (True, [0, 0, 0])

    eqs20 = [Eq(Derivative(x(t), t), 4*x(t) - y(t) - 2*z(t)),
             Eq(Derivative(y(t), t), 2*x(t) + y(t) - 2*z(t)),
             Eq(Derivative(z(t), t), 5*x(t) - 3*z(t))]
    sol20 = [Eq(x(t), C1*exp(2*t) - sin(t)*(C2*Rational(3, 5) + C3/5) - cos(t)*(C2/5 + C3*Rational(-3, 5))),
             Eq(y(t), -sin(t)*(C2*Rational(3, 5) + C3/5) - cos(t)*(C2/5 + C3*Rational(-3, 5))),
             Eq(z(t), C1*exp(2*t) - C2*sin(t) + C3*cos(t))]
    assert dsolve(eqs20) == sol20
    assert checksysodesol(eqs20, sol20) == (True, [0, 0, 0])

    eq21 = (Eq(diff(x(t), t), 9*y(t)), Eq(diff(y(t), t), 12*x(t)))
    sol21 = [Eq(x(t), -sqrt(3)*C1*exp(-6*sqrt(3)*t)/2 + sqrt(3)*C2*exp(6*sqrt(3)*t)/2),
             Eq(y(t), C1*exp(-6*sqrt(3)*t) + C2*exp(6*sqrt(3)*t))]

    assert dsolve(eq21) == sol21
    assert checksysodesol(eq21, sol21) == (True, [0, 0])

    eqs22 = [Eq(Derivative(x(t), t), 2*x(t) + 4*y(t)),
             Eq(Derivative(y(t), t), 12*x(t) + 41*y(t))]
    sol22 = [Eq(x(t), C1*(39 - sqrt(1713))*exp(t*(sqrt(1713) + 43)/2)*Rational(-1, 24) + C2*(39 +
              sqrt(1713))*exp(t*(43 - sqrt(1713))/2)*Rational(-1, 24)),
             Eq(y(t), C1*exp(t*(sqrt(1713) + 43)/2) + C2*exp(t*(43 - sqrt(1713))/2))]
    assert dsolve(eqs22) == sol22
    assert checksysodesol(eqs22, sol22) == (True, [0, 0])

    eqs23 = [Eq(Derivative(x(t), t), x(t) + y(t)),
             Eq(Derivative(y(t), t), -2*x(t) + 2*y(t))]
    sol23 = [Eq(x(t), (C1/4 + sqrt(7)*C2/4)*cos(sqrt(7)*t/2)*exp(t*Rational(3, 2)) +
              sin(sqrt(7)*t/2)*(sqrt(7)*C1/4 + C2*Rational(-1, 4))*exp(t*Rational(3, 2))),
             Eq(y(t), C1*cos(sqrt(7)*t/2)*exp(t*Rational(3, 2)) - C2*sin(sqrt(7)*t/2)*exp(t*Rational(3, 2)))]
    assert dsolve(eqs23) == sol23
    assert checksysodesol(eqs23, sol23) == (True, [0, 0])

    # Regression test case for issue #15474
    # https://github.com/sympy/sympy/issues/15474
    a = Symbol("a", real=True)
    eq24 = [x(t).diff(t) - a*y(t), y(t).diff(t) + a*x(t)]
    sol24 = [Eq(x(t), C1*sin(a*t) + C2*cos(a*t)), Eq(y(t), C1*cos(a*t) - C2*sin(a*t))]
    assert dsolve(eq24) == sol24
    assert checksysodesol(eq24, sol24) == (True, [0, 0])

    # Regression test case for issue #19150
    # https://github.com/sympy/sympy/issues/19150
    eqs25 = [Eq(Derivative(f(t), t), 0),
             Eq(Derivative(g(t), t), (f(t) - 2*g(t) + x(t))/(b*c)),
             Eq(Derivative(x(t), t), (g(t) - 2*x(t) + y(t))/(b*c)),
             Eq(Derivative(y(t), t), (h(t) + x(t) - 2*y(t))/(b*c)),
             Eq(Derivative(h(t), t), 0)]
    sol25 = [Eq(f(t), -3*C1 + 4*C2),
             Eq(g(t), -2*C1 + 3*C2 - C3*exp(-2*t/(b*c)) + C4*exp(-t*(sqrt(2) + 2)/(b*c)) + C5*exp(-t*(2 -
              sqrt(2))/(b*c))),
             Eq(x(t), -C1 + 2*C2 - sqrt(2)*C4*exp(-t*(sqrt(2) + 2)/(b*c)) + sqrt(2)*C5*exp(-t*(2 -
              sqrt(2))/(b*c))),
             Eq(y(t), C2 + C3*exp(-2*t/(b*c)) + C4*exp(-t*(sqrt(2) + 2)/(b*c)) + C5*exp(-t*(2 - sqrt(2))/(b*c))),
             Eq(h(t), C1)]
    assert dsolve(eqs25) == sol25
    assert checksysodesol(eqs25, sol25) == (True, [0, 0, 0, 0, 0])

    eq26 = [Eq(Derivative(f(t), t), 2*f(t)), Eq(Derivative(g(t), t), 3*f(t) + 7*g(t))]
    sol26 = [Eq(f(t), -5*C1*exp(2*t)/3), Eq(g(t), C1*exp(2*t) + C2*exp(7*t))]
    assert dsolve(eq26) == sol26
    assert checksysodesol(eq26, sol26) == (True, [0, 0])

    eq27 = [Eq(Derivative(f(t), t), -9*I*f(t) - 4*g(t)), Eq(Derivative(g(t), t), -4*I*g(t))]
    sol27 = [Eq(f(t), 4*I*C1*exp(-4*I*t)/5 + C2*exp(-9*I*t)), Eq(g(t), C1*exp(-4*I*t))]
    assert dsolve(eq27) == sol27
    assert checksysodesol(eq27, sol27) == (True, [0, 0])

    eq28 = [Eq(Derivative(f(t), t), -9*I*f(t)), Eq(Derivative(g(t), t), -4*I*g(t))]
    sol28 = [Eq(f(t), C1*exp(-9*I*t)), Eq(g(t), C2*exp(-4*I*t))]
    assert dsolve(eq28) == sol28
    assert checksysodesol(eq28, sol28) == (True, [0, 0])

    eq29 = [Eq(Derivative(f(t), t), 0), Eq(Derivative(g(t), t), 0)]
    sol29 = [Eq(f(t), C1), Eq(g(t), C2)]
    assert dsolve(eq29) == sol29
    assert checksysodesol(eq29, sol29) == (True, [0, 0])

    eq30 = [Eq(Derivative(f(t), t), f(t)), Eq(Derivative(g(t), t), 0)]
    sol30 = [Eq(f(t), C1*exp(t)), Eq(g(t), C2)]
    assert dsolve(eq30) == sol30
    assert checksysodesol(eq30, sol30) == (True, [0, 0])

    eq31 = [Eq(Derivative(f(t), t), g(t)), Eq(Derivative(g(t), t), 0)]
    sol31 = [Eq(f(t), C1 + C2*t), Eq(g(t), C2)]
    assert dsolve(eq31) == sol31
    assert checksysodesol(eq31, sol31) == (True, [0, 0])

    eq32 = [Eq(Derivative(f(t), t), 0), Eq(Derivative(g(t), t), f(t))]
    sol32 = [Eq(f(t), C1), Eq(g(t), C1*t + C2)]
    assert dsolve(eq32) == sol32
    assert checksysodesol(eq32, sol32) == (True, [0, 0])

    eq33 = [Eq(Derivative(f(t), t), 0), Eq(Derivative(g(t), t), g(t))]
    sol33 = [Eq(f(t), C1), Eq(g(t), C2*exp(t))]
    assert dsolve(eq33) == sol33
    assert checksysodesol(eq33, sol33) == (True, [0, 0])

    eq34 = [Eq(Derivative(f(t), t), f(t)), Eq(Derivative(g(t), t), I*g(t))]
    sol34 = [Eq(f(t), C1*exp(t)), Eq(g(t), C2*exp(I*t))]
    assert dsolve(eq34) == sol34
    assert checksysodesol(eq34, sol34) == (True, [0, 0])

    eq35 = [Eq(Derivative(f(t), t), I*f(t)), Eq(Derivative(g(t), t), -I*g(t))]
    sol35 = [Eq(f(t), C1*exp(I*t)), Eq(g(t), C2*exp(-I*t))]
    assert dsolve(eq35) == sol35
    assert checksysodesol(eq35, sol35) == (True, [0, 0])

    eq36 = [Eq(Derivative(f(t), t), I*g(t)), Eq(Derivative(g(t), t), 0)]
    sol36 = [Eq(f(t), I*C1 + I*C2*t), Eq(g(t), C2)]
    assert dsolve(eq36) == sol36
    assert checksysodesol(eq36, sol36) == (True, [0, 0])

    eq37 = [Eq(Derivative(f(t), t), I*g(t)), Eq(Derivative(g(t), t), I*f(t))]
    sol37 = [Eq(f(t), -C1*exp(-I*t) + C2*exp(I*t)), Eq(g(t), C1*exp(-I*t) + C2*exp(I*t))]
    assert dsolve(eq37) == sol37
    assert checksysodesol(eq37, sol37) == (True, [0, 0])

    # Multiple systems
    eq1 = [Eq(Derivative(f(t), t)**2, g(t)**2), Eq(-f(t) + Derivative(g(t), t), 0)]
    sol1 = [[Eq(f(t), -C1*sin(t) - C2*cos(t)),
             Eq(g(t), C1*cos(t) - C2*sin(t))],
            [Eq(f(t), -C1*exp(-t) + C2*exp(t)),
             Eq(g(t), C1*exp(-t) + C2*exp(t))]]
    assert dsolve(eq1) == sol1
    for sol in sol1:
        assert checksysodesol(eq1, sol) == (True, [0, 0])

