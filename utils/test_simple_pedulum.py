
def test_simple_pedulum():
    l, m, g = symbols('l m g')
    with warns_deprecated_sympy():
        C = Body('C')
        b = Body('b', mass=m)
    q = dynamicsymbols('q')
    P = PinJoint('P', C, b, speeds=q.diff(t), coordinates=q,
                 child_point=-l * b.x, joint_axis=C.z)
    b.potential_energy = - m * g * l * cos(q)
    with warns_deprecated_sympy():
        method = JointsMethod(C, P)
    method.form_eoms(LagrangesMethod)
    rhs = method.rhs()
    assert rhs[1] == -g*sin(q)/l

