
def test_linearize_pendulum_kane_nonminimal():
    # Create generalized coordinates and speeds for this non-minimal realization
    # q1, q2 = N.x and N.y coordinates of pendulum
    # u1, u2 = N.x and N.y velocities of pendulum
    q1, q2 = dynamicsymbols('q1:3')
    q1d, q2d = dynamicsymbols('q1:3', level=1)
    u1, u2 = dynamicsymbols('u1:3')
    u1d, u2d = dynamicsymbols('u1:3', level=1)
    L, m, t = symbols('L, m, t')
    g = 9.8

    # Compose world frame
    N = ReferenceFrame('N')
    pN = Point('N*')
    pN.set_vel(N, 0)

    # A.x is along the pendulum
    theta1 = atan(q2/q1)
    A = N.orientnew('A', 'axis', [theta1, N.z])

    # Locate the pendulum mass
    P = pN.locatenew('P1', q1*N.x + q2*N.y)
    pP = Particle('pP', P, m)

    # Calculate the kinematic differential equations
    kde = Matrix([q1d - u1,
                  q2d - u2])
    dq_dict = solve(kde, [q1d, q2d])

    # Set velocity of point P
    P.set_vel(N, P.pos_from(pN).dt(N).subs(dq_dict))

    # Configuration constraint is length of pendulum
    f_c = Matrix([P.pos_from(pN).magnitude() - L])

    # Velocity constraint is that the velocity in the A.x direction is
    # always zero (the pendulum is never getting longer).
    f_v = Matrix([P.vel(N).express(A).dot(A.x)])
    f_v.simplify()

    # Acceleration constraints is the time derivative of the velocity constraint
    f_a = f_v.diff(t)
    f_a.simplify()

    # Input the force resultant at P
    R = m*g*N.x

    # Derive the equations of motion using the KanesMethod class.
    KM = KanesMethod(N, q_ind=[q2], u_ind=[u2], q_dependent=[q1],
            u_dependent=[u1], configuration_constraints=f_c,
            velocity_constraints=f_v, acceleration_constraints=f_a, kd_eqs=kde)
    (fr, frstar) = KM.kanes_equations([pP], [(P, R)])

    # Set the operating point to be straight down, and non-moving
    q_op = {q1: L, q2: 0}
    u_op = {u1: 0, u2: 0}
    ud_op = {u1d: 0, u2d: 0}

    A, B, inp_vec = KM.linearize(op_point=[q_op, u_op, ud_op], A_and_B=True,
                                 simplify=True)

    assert A.expand() == Matrix([[0, 1], [-9.8/L, 0]])
    assert B == Matrix([])


    # symengine doesn't support method='GJ'
    A, B, inp_vec = KM.linearize(op_point=[q_op, u_op, ud_op], A_and_B=True,
                                simplify=True, linear_solver='GJ')

    assert A.expand() == Matrix([[0, 1], [-9.8/L, 0]])
    assert B == Matrix([])

    A, B, inp_vec = KM.linearize(op_point=[q_op, u_op, ud_op],
                                 A_and_B=True,
                                 simplify=True,
                                 linear_solver=lambda A, b: A.LUsolve(b))

    assert A.expand() == Matrix([[0, 1], [-9.8/L, 0]])
    assert B == Matrix([])

