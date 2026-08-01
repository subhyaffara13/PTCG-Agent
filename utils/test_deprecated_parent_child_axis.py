
def test_deprecated_parent_child_axis():
    q, u = dynamicsymbols('q_J, u_J')
    N, A, P, C = _generate_body()
    with warns_deprecated_sympy():
        PinJoint('J', P, C, child_axis=-A.x)
    assert (-A.x).angle_between(N.x) == 0
    assert -A.x.express(N) == N.x
    assert A.dcm(N) == Matrix([[-1, 0, 0],
                               [0, -cos(q), -sin(q)],
                               [0, -sin(q), cos(q)]])
    assert A.ang_vel_in(N) == u * N.x
    assert A.ang_vel_in(N).magnitude() == sqrt(u ** 2)

    N, A, P, C = _generate_body()
    with warns_deprecated_sympy():
        PrismaticJoint('J', P, C, parent_axis=P.x + P.y)
    assert (A.x).angle_between(N.x + N.y) == 0
    assert A.x.express(N) == (N.x + N.y) / sqrt(2)
    assert A.dcm(N) == Matrix([[sqrt(2) / 2, sqrt(2) / 2, 0],
                               [-sqrt(2) / 2, sqrt(2) / 2, 0], [0, 0, 1]])
    assert A.ang_vel_in(N) == Vector(0)

