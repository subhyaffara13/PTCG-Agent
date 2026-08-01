
def test_deprecated_joint_pos():
    N, A, P, C = _generate_body()
    with warns_deprecated_sympy():
        pin = PinJoint('J', P, C, parent_joint_pos=N.x + N.y,
                       child_joint_pos=C.y - C.z)
    assert pin.parent_point.pos_from(P.masscenter) == N.x + N.y
    assert pin.child_point.pos_from(C.masscenter) == C.y - C.z

    N, A, P, C = _generate_body()
    with warns_deprecated_sympy():
        slider = PrismaticJoint('J', P, C, parent_joint_pos=N.z + N.y,
                                child_joint_pos=C.y - C.x)
    assert slider.parent_point.pos_from(P.masscenter) == N.z + N.y
    assert slider.child_point.pos_from(C.masscenter) == C.y - C.x

