
def test_linearize_pendulum_lagrange_nonminimal():
    q1, q2 = dynamicsymbols('q1:3')
    q1d, q2d = dynamicsymbols('q1:3', level=1)
    L, m, t = symbols('L, m, t')
    g = 9.8
    # Compose World Frame
    N = ReferenceFrame('N')
    pN = Point('N*')
    pN.set_vel(N, 0)
    # A.x is along the pendulum
    theta1 = atan(q2/q1)
    A = N.orientnew('A', 'axis', [theta1, N.z])
    # Create point P, the pendulum mass
    P = pN.locatenew('P1', q1*N.x + q2*N.y)
    P.set_vel(N, P.pos_from(pN).dt(N))
    pP = Particle('pP', P, m)
    # Constraint Equations
    f_c = Matrix([q1**2 + q2**2 - L**2])
    # Calculate the lagrangian, and form the equations of motion
    Lag = Lagrangian(N, pP)
    LM = LagrangesMethod(Lag, [q1, q2], hol_coneqs=f_c, forcelist=[(P, m*g*N.x)], frame=N)
    LM.form_lagranges_equations()
    # Compose operating point
    op_point = {q1: L, q2: 0, q1d: 0, q2d: 0, q1d.diff(t): 0, q2d.diff(t): 0}
    # Solve for multiplier operating point
    lam_op = LM.solve_multipliers(op_point=op_point)
    op_point.update(lam_op)
    # Perform the Linearization
    A, B, inp_vec = LM.linearize([q2], [q2d], [q1], [q1d],
            op_point=op_point, A_and_B=True)
    assert simplify(A) == Matrix([[0, 1], [-9.8/L, 0]])
    assert B == Matrix([])

    # Check if passing a function to linear_solver works
    A, B, inp_vec = LM.linearize([q2], [q2d], [q1], [q1d], op_point=op_point,
                                 A_and_B=True, linear_solver=lambda A, b:
                                 A.LUsolve(b))
    assert simplify(A) == Matrix([[0, 1], [-9.8/L, 0]])
    assert B == Matrix([])

