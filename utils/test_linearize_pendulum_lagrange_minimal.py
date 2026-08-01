
def test_linearize_pendulum_lagrange_minimal():
    q1 = dynamicsymbols('q1')                     # angle of pendulum
    q1d = dynamicsymbols('q1', 1)                 # Angular velocity
    L, m, t = symbols('L, m, t')
    g = 9.8

    # Compose world frame
    N = ReferenceFrame('N')
    pN = Point('N*')
    pN.set_vel(N, 0)

    # A.x is along the pendulum
    A = N.orientnew('A', 'axis', [q1, N.z])
    A.set_ang_vel(N, q1d*N.z)

    # Locate point P relative to the origin N*
    P = pN.locatenew('P', L*A.x)
    P.v2pt_theory(pN, N, A)
    pP = Particle('pP', P, m)

    # Solve for eom with Lagranges method
    Lag = Lagrangian(N, pP)
    LM = LagrangesMethod(Lag, [q1], forcelist=[(P, m*g*N.x)], frame=N)
    LM.form_lagranges_equations()

    # Linearize
    A, B, inp_vec = LM.linearize([q1], [q1d], A_and_B=True)

    assert simplify(A) == Matrix([[0, 1], [-9.8*cos(q1)/L, 0]])
    assert B == Matrix([])

    # Check an alternative solver
    A, B, inp_vec = LM.linearize([q1], [q1d], A_and_B=True, linear_solver='GJ')

    assert simplify(A) == Matrix([[0, 1], [-9.8*cos(q1)/L, 0]])
    assert B == Matrix([])

