
def test_locate_joint_frame():
    # Test rotated frame and default
    N, A, P, C = _generate_body()
    parent_interframe = ReferenceFrame('int_frame')
    parent_interframe.orient_axis(N, N.z, 1)
    joint = PinJoint('J', P, C, parent_interframe=parent_interframe)
    assert joint.parent_interframe == parent_interframe
    assert joint.parent_interframe.ang_vel_in(N) == 0
    assert joint.child_interframe == A
    # Test time varying orientations
    q = dynamicsymbols('q')
    N, A, P, C = _generate_body()
    parent_interframe = ReferenceFrame('int_frame')
    parent_interframe.orient_axis(N, N.z, q)
    raises(ValueError,
           lambda: PinJoint('J', P, C, parent_interframe=parent_interframe))
    # Test undefined frame
    N, A, P, C = _generate_body()
    child_interframe = ReferenceFrame('int_frame')
    child_interframe.orient_axis(N, N.z, 1)  # Defined with respect to parent
    raises(ValueError,
           lambda: PinJoint('J', P, C, child_interframe=child_interframe))

