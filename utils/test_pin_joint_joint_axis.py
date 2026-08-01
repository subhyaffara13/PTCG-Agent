
def test_pin_joint_joint_axis():
    q, u = dynamicsymbols('q, u')
    # Check parent as reference
    N, A, P, C, Pint, Cint = _generate_body(True)
    pin = PinJoint('J', P, C, q, u, parent_interframe=Pint,
                   child_interframe=Cint, joint_axis=P.y)
    assert pin.joint_axis == P.y
    assert N.dcm(A) == Matrix([[sin(q), 0, cos(q)], [0, -1, 0],
                               [cos(q), 0, -sin(q)]])
    # Check parent_interframe as reference
    N, A, P, C, Pint, Cint = _generate_body(True)
    pin = PinJoint('J', P, C, q, u, parent_interframe=Pint,
                   child_interframe=Cint, joint_axis=Pint.y)
    assert pin.joint_axis == Pint.y
    assert N.dcm(A) == Matrix([[-sin(q), 0, cos(q)], [0, -1, 0],
                               [cos(q), 0, sin(q)]])
    # Check combination of joint_axis with interframes supplied as vectors (2x)
    N, A, P, C = _generate_body()
    pin = PinJoint('J', P, C, q, u, parent_interframe=N.z,
                   child_interframe=-C.z, joint_axis=N.z)
    assert pin.joint_axis == N.z
    assert N.dcm(A) == Matrix([[-cos(q), -sin(q), 0], [-sin(q), cos(q), 0],
                               [0, 0, -1]])
    N, A, P, C = _generate_body()
    pin = PinJoint('J', P, C, q, u, parent_interframe=N.z,
                   child_interframe=-C.z, joint_axis=N.x)
    assert pin.joint_axis == N.x
    assert N.dcm(A) == Matrix([[-1, 0, 0], [0, cos(q), sin(q)],
                               [0, sin(q), -cos(q)]])
    # Check time varying axis
    N, A, P, C, Pint, Cint = _generate_body(True)
    raises(ValueError, lambda: PinJoint('J', P, C,
                                        joint_axis=cos(q) * N.x + sin(q) * N.y))
    # Check joint_axis provided in child frame
    raises(ValueError, lambda: PinJoint('J', P, C, joint_axis=C.x))
    # Check some invalid combinations
    raises(ValueError, lambda: PinJoint('J', P, C, joint_axis=P.x + C.y))
    raises(ValueError, lambda: PinJoint(
        'J', P, C, parent_interframe=Pint, child_interframe=Cint,
        joint_axis=Pint.x + C.y))
    raises(ValueError, lambda: PinJoint(
        'J', P, C, parent_interframe=Pint, child_interframe=Cint,
        joint_axis=P.x + Cint.y))
    # Check valid special combination
    N, A, P, C, Pint, Cint = _generate_body(True)
    PinJoint('J', P, C, parent_interframe=Pint, child_interframe=Cint,
             joint_axis=Pint.x + P.y)
    # Check invalid zero vector
    raises(Exception, lambda: PinJoint(
        'J', P, C, parent_interframe=Pint, child_interframe=Cint,
        joint_axis=Vector(0)))
    raises(Exception, lambda: PinJoint(
        'J', P, C, parent_interframe=Pint, child_interframe=Cint,
        joint_axis=P.y + Pint.y))

