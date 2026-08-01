
def test_StateSpace_dsolve():
    # https://web.mit.edu/2.14/www/Handouts/StateSpaceResponse.pdf
    # https://lpsa.swarthmore.edu/Transient/TransMethSS.html
    A1 = Matrix([[0, 1], [-2, -3]])
    B1 = Matrix([[0], [1]])
    C1 = Matrix([[1, -1]])
    D1 = Matrix([0])
    I1 = Matrix([[1], [2]])
    t = symbols('t')
    ss1 = StateSpace(A1, B1, C1, D1)

    # Zero input and Zero initial conditions
    assert ss1.dsolve() == Matrix([[0]])
    assert ss1.dsolve(initial_conditions=I1) == Matrix([[8*exp(-t) - 9*exp(-2*t)]])

    A2 = Matrix([[-2, 0], [1, -1]])
    C2 = eye(2,2)
    I2 = Matrix([2, 3])
    ss2 = StateSpace(A=A2, C=C2)
    assert ss2.dsolve(initial_conditions=I2) == Matrix([[2*exp(-2*t)], [5*exp(-t) - 2*exp(-2*t)]])

    A3 = Matrix([[-1, 1], [-4, -4]])
    B3 = Matrix([[0], [4]])
    C3 = Matrix([[0, 1]])
    D3 = Matrix([0])
    U3 = Matrix([10])
    ss3 = StateSpace(A3, B3, C3, D3)
    op = ss3.dsolve(input_vector=U3, var=t)
    assert str(op.simplify().expand().evalf()[0]) == str(5.0 + 20.7880460155075*exp(-5*t/2)*sin(sqrt(7)*t/2)
                                            - 5.0*exp(-5*t/2)*cos(sqrt(7)*t/2))

    # Test with Heaviside as input
    A4 = Matrix([[-1, 1], [-4, -4]])
    B4 = Matrix([[0], [4]])
    C4 = Matrix([[0, 1]])
    U4 = Matrix([[10*Heaviside(t)]])
    ss4 = StateSpace(A4, B4, C4)
    op4 = str(ss4.dsolve(var=t, input_vector=U4)[0].simplify().expand().evalf())
    assert op4 == str(5.0*Heaviside(t) + 20.7880460155075*exp(-5*t/2)*sin(sqrt(7)*t/2)*Heaviside(t)
                                            - 5.0*exp(-5*t/2)*cos(sqrt(7)*t/2)*Heaviside(t))

    # Test with Symbolic Matrices
    m, a, x0 = symbols('m a x_0')
    A5 = Matrix([[0, 1], [0, 0]])
    B5 = Matrix([[0], [1 / m]])
    C5 = Matrix([[1, 0]])
    I5 = Matrix([[x0], [0]])
    U5 = Matrix([[exp(-a * t)]])
    ss5 = StateSpace(A5, B5, C5)
    op5 = ss5.dsolve(initial_conditions=I5, input_vector=U5, var=t).simplify()
    assert op5[0].args[0][0] == x0 + t/(a*m) - 1/(a**2*m) + exp(-a*t)/(a**2*m)
    a11, a12, a21, a22, b1, b2, c1, c2, i1, i2 = symbols('a_11 a_12 a_21 a_22 b_1 b_2 c_1 c_2 i_1 i_2')
    A6 = Matrix([[a11, a12], [a21, a22]])
    B6 = Matrix([b1, b2])
    C6 = Matrix([[c1, c2]])
    I6 = Matrix([i1, i2])
    ss6 = StateSpace(A6, B6, C6)
    expr6 = ss6.dsolve(initial_conditions=I6)[0]
    expr6 = expr6.subs([(a11, 0), (a12, 1), (a21, -2), (a22, -3), (b1, 0), (b2, 1), (c1, 1), (c2, -1), (i1, 1), (i2, 2)])
    assert expr6 == 8*exp(-t) - 9*exp(-2*t)

