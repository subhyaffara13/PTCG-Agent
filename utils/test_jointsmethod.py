
def test_jointsmethod():
    with warns_deprecated_sympy():
        P = Body('P')
        C = Body('C')
    Pin = PinJoint('P1', P, C)
    C_ixx, g = symbols('C_ixx g')
    q, u = dynamicsymbols('q_P1, u_P1')
    P.apply_force(g*P.y)
    with warns_deprecated_sympy():
        method = JointsMethod(P, Pin)
    assert method.frame == P.frame
    assert method.bodies == [C, P]
    assert method.loads == [(P.masscenter, g*P.frame.y)]
    assert method.q == Matrix([q])
    assert method.u == Matrix([u])
    assert method.kdes == Matrix([u - q.diff()])
    soln = method.form_eoms()
    assert soln == Matrix([[-C_ixx*u.diff()]])
    assert method.forcing_full == Matrix([[u], [0]])
    assert method.mass_matrix_full == Matrix([[1, 0], [0, C_ixx]])
    assert isinstance(method.method, KanesMethod)

