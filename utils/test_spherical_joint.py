
def test_spherical_joint():
    N, A, P, C = _generate_body()
    q0, q1, q2, u0, u1, u2 = dynamicsymbols('q0:3_S, u0:3_S')
    S = SphericalJoint('S', P, C)
    assert S.name == 'S'
    assert S.parent == P
    assert S.child == C
    assert S.coordinates == Matrix([q0, q1, q2])
    assert S.speeds == Matrix([u0, u1, u2])
    assert S.kdes == Matrix([u0 - q0.diff(t), u1 - q1.diff(t), u2 - q2.diff(t)])
    assert S.child_point.pos_from(C.masscenter) == Vector(0)
    assert S.parent_point.pos_from(P.masscenter) == Vector(0)
    assert S.parent_point.pos_from(S.child_point) == Vector(0)
    assert P.masscenter.pos_from(C.masscenter) == Vector(0)
    assert C.masscenter.vel(N) == Vector(0)
    assert N.ang_vel_in(A) == (-u0 * cos(q1) * cos(q2) - u1 * sin(q2)) * A.x + (
            u0 * sin(q2) * cos(q1) - u1 * cos(q2)) * A.y + (
                   -u0 * sin(q1) - u2) * A.z
    assert A.ang_vel_in(N) == (u0 * cos(q1) * cos(q2) + u1 * sin(q2)) * A.x + (
            -u0 * sin(q2) * cos(q1) + u1 * cos(q2)) * A.y + (
                   u0 * sin(q1) + u2) * A.z
    assert S.__str__() == 'SphericalJoint: S  parent: P  child: C'
    assert S._rot_type == 'BODY'
    assert S._rot_order == 123
    assert S._amounts is None

