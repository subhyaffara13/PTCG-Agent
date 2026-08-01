
def test_spherical_joint_speeds_as_derivative_terms():
    # This tests checks whether the system remains valid if the user chooses to
    # pass the derivative of the generalized coordinates as generalized speeds
    q0, q1, q2 = dynamicsymbols('q0:3')
    u0, u1, u2 = dynamicsymbols('q0:3', 1)
    N, A, P, C = _generate_body()
    S = SphericalJoint('S', P, C, coordinates=[q0, q1, q2], speeds=[u0, u1, u2])
    assert S.coordinates == Matrix([q0, q1, q2])
    assert S.speeds == Matrix([u0, u1, u2])
    assert S.kdes == Matrix([0, 0, 0])
    assert N.ang_vel_in(A) == (-u0 * cos(q1) * cos(q2) - u1 * sin(q2)) * A.x + (
        u0 * sin(q2) * cos(q1) - u1 * cos(q2)) * A.y + (
               -u0 * sin(q1) - u2) * A.z

