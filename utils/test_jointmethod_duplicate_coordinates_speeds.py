
def test_jointmethod_duplicate_coordinates_speeds():
    with warns_deprecated_sympy():
        P = Body('P')
        C = Body('C')
        T = Body('T')
    q, u = dynamicsymbols('q u')
    P1 = PinJoint('P1', P, C, q)
    P2 = PrismaticJoint('P2', C, T, q)
    with warns_deprecated_sympy():
        raises(ValueError, lambda: JointsMethod(P, P1, P2))

    P1 = PinJoint('P1', P, C, speeds=u)
    P2 = PrismaticJoint('P2', C, T, speeds=u)
    with warns_deprecated_sympy():
        raises(ValueError, lambda: JointsMethod(P, P1, P2))

    P1 = PinJoint('P1', P, C, q, u)
    P2 = PrismaticJoint('P2', C, T, q, u)
    with warns_deprecated_sympy():
        raises(ValueError, lambda: JointsMethod(P, P1, P2))

