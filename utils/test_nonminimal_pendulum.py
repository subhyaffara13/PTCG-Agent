
def test_nonminimal_pendulum():
    q1, q2 = dynamicsymbols('q1:3')
    q1d, q2d = dynamicsymbols('q1:3', level=1)
    L, m, t = symbols('L, m, t')
    g = 9.8
    # Compose World Frame
    N = ReferenceFrame('N')
    pN = Point('N*')
    pN.set_vel(N, 0)
    # Create point P, the pendulum mass
    P = pN.locatenew('P1', q1*N.x + q2*N.y)
    P.set_vel(N, P.pos_from(pN).dt(N))
    pP = Particle('pP', P, m)
    # Constraint Equations
    f_c = Matrix([q1**2 + q2**2 - L**2])
    # Calculate the lagrangian, and form the equations of motion
    Lag = Lagrangian(N, pP)
    LM = LagrangesMethod(Lag, [q1, q2], hol_coneqs=f_c,
            forcelist=[(P, m*g*N.x)], frame=N)
    LM.form_lagranges_equations()
    # Check solution
    lam1 = LM.lam_vec[0, 0]
    eom_sol = Matrix([[m*Derivative(q1, t, t) - 9.8*m + 2*lam1*q1],
                      [m*Derivative(q2, t, t) + 2*lam1*q2]])
    assert LM.eom == eom_sol
    # Check multiplier solution
    lam_sol = Matrix([(19.6*q1 + 2*q1d**2 + 2*q2d**2)/(4*q1**2/m + 4*q2**2/m)])
    assert simplify(LM.solve_multipliers(sol_type='Matrix')) == simplify(lam_sol)

