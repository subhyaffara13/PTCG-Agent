
def test_apply_torque():
    t = symbols('t')
    q = dynamicsymbols('q')
    with warns_deprecated_sympy():
        B1 = Body('B1')
        B2 = Body('B2')
    N = ReferenceFrame('N')
    torque = t*q*N.x

    B1.apply_torque(torque, B2) #Applying equal and opposite torque
    assert B1.loads == [(B1.frame, torque)]
    assert B2.loads == [(B2.frame, -torque)]

    torque2 = t*N.y
    B1.apply_torque(torque2)
    assert B1.loads == [(B1.frame, torque+torque2)]

