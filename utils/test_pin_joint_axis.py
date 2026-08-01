
def test_pin_joint_axis():
    q, u = dynamicsymbols('q u')
    # Test default joint axis
    N, A, P, C, Pint, Cint = _generate_body(True)
    J = PinJoint('J', P, C, q, u, parent_interframe=Pint, child_interframe=Cint)
    assert J.joint_axis == Pint.x
    # Test for the same joint axis expressed in different frames
    N_R_A = Matrix([[0, sin(q), cos(q)],
                    [0, -cos(q), sin(q)],
                    [1, 0, 0]])
    N, A, P, C, Pint, Cint = _generate_body(True)
    PinJoint('J', P, C, q, u, parent_interframe=Pint, child_interframe=Cint,
             joint_axis=N.z)
    assert N.dcm(A) == N_R_A
    N, A, P, C, Pint, Cint = _generate_body(True)
    PinJoint('J', P, C, q, u, parent_interframe=Pint, child_interframe=Cint,
             joint_axis=-Pint.z)
    assert N.dcm(A) == N_R_A
    # Test time varying joint axis
    N, A, P, C, Pint, Cint = _generate_body(True)
    raises(ValueError, lambda: PinJoint('J', P, C, joint_axis=q * N.z))

