
def test_linearize_pendulum_kane_minimal():
    q1 = dynamicsymbols('q1')                     # angle of pendulum
    u1 = dynamicsymbols('u1')                     # Angular velocity
    q1d = dynamicsymbols('q1', 1)                 # Angular velocity
    L, m, t = symbols('L, m, t')
    g = 9.8

    # Compose world frame
    N = ReferenceFrame('N')
    pN = Point('N*')
    pN.set_vel(N, 0)

    # A.x is along the pendulum
    A = N.orientnew('A', 'axis', [q1, N.z])
    A.set_ang_vel(N, u1*N.z)

    # Locate point P relative to the origin N*
    P = pN.locatenew('P', L*A.x)
    P.v2pt_theory(pN, N, A)
    pP = Particle('pP', P, m)

    # Create Kinematic Differential Equations
    kde = Matrix([q1d - u1])

    # Input the force resultant at P
    R = m*g*N.x

    # Solve for eom with kanes method
    KM = KanesMethod(N, q_ind=[q1], u_ind=[u1], kd_eqs=kde)
    (fr, frstar) = KM.kanes_equations([pP], [(P, R)])

    # Linearize
    A, B, inp_vec = KM.linearize(A_and_B=True, simplify=True)

    assert A == Matrix([[0, 1], [-9.8*cos(q1)/L, 0]])
    assert B == Matrix([])

