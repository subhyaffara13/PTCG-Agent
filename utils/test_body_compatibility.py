
def test_body_compatibility():
    m, l = symbols('m l')
    C_frame = ReferenceFrame('C')
    with warns_deprecated_sympy():
        P = Body('P')
        C = Body('C', mass=m, frame=C_frame)
    q, u = dynamicsymbols('q, u')
    PinJoint('J', P, C, q, u, child_point=l * C_frame.y)
    assert C.frame == C_frame
    assert P.frame.name == 'P_frame'
    assert C.masscenter.pos_from(P.masscenter) == -l * C.y
    assert C.frame.dcm(P.frame) == Matrix([[1, 0, 0],
                                           [0, cos(q), sin(q)],
                                           [0, -sin(q), cos(q)]])
    assert C.masscenter.vel(P.frame) == -l * u * C.z

