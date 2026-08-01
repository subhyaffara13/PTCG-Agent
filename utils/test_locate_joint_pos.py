
def test_locate_joint_pos():
    # Test Vector and default
    N, A, P, C = _generate_body()
    joint = PinJoint('J', P, C, parent_point=N.y + N.z)
    assert joint.parent_point.name == 'J_P_joint'
    assert joint.parent_point.pos_from(P.masscenter) == N.y + N.z
    assert joint.child_point == C.masscenter
    # Test Point objects
    N, A, P, C = _generate_body()
    parent_point = P.masscenter.locatenew('p', N.y + N.z)
    joint = PinJoint('J', P, C, parent_point=parent_point,
                     child_point=C.masscenter)
    assert joint.parent_point == parent_point
    assert joint.child_point == C.masscenter
    # Check invalid type
    N, A, P, C = _generate_body()
    raises(TypeError,
           lambda: PinJoint('J', P, C, parent_point=N.x.to_matrix(N)))
    # Test time varying positions
    q = dynamicsymbols('q')
    N, A, P, C = _generate_body()
    raises(ValueError, lambda: PinJoint('J', P, C, parent_point=q * N.x))
    N, A, P, C = _generate_body()
    child_point = C.masscenter.locatenew('p', q * A.y)
    raises(ValueError, lambda: PinJoint('J', P, C, child_point=child_point))
    # Test undefined position
    child_point = Point('p')
    raises(ValueError, lambda: PinJoint('J', P, C, child_point=child_point))

