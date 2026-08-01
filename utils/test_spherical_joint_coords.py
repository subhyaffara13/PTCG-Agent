
def test_spherical_joint_coords():
    q0s, q1s, q2s, u0s, u1s, u2s = dynamicsymbols('q0:3_S, u0:3_S')
    q0, q1, q2, q3, u0, u1, u2, u4 = dynamicsymbols('q0:4, u0:4')
    # Test coordinates as list
    N, A, P, C = _generate_body()
    S = SphericalJoint('S', P, C, [q0, q1, q2], [u0, u1, u2])
    assert S.coordinates == Matrix([q0, q1, q2])
    assert S.speeds == Matrix([u0, u1, u2])
    # Test coordinates as Matrix
    N, A, P, C = _generate_body()
    S = SphericalJoint('S', P, C, Matrix([q0, q1, q2]),
                       Matrix([u0, u1, u2]))
    assert S.coordinates == Matrix([q0, q1, q2])
    assert S.speeds == Matrix([u0, u1, u2])
    # Test too few generalized coordinates
    N, A, P, C = _generate_body()
    raises(ValueError,
           lambda: SphericalJoint('S', P, C, Matrix([q0, q1]), Matrix([u0])))
    # Test too many generalized coordinates
    raises(ValueError, lambda: SphericalJoint(
        'S', P, C, Matrix([q0, q1, q2, q3]), Matrix([u0, u1, u2])))
    raises(ValueError, lambda: SphericalJoint(
        'S', P, C, Matrix([q0, q1, q2]), Matrix([u0, u1, u2, u4])))

