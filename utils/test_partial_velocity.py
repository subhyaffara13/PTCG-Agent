
def test_partial_velocity():

    N = ReferenceFrame('N')
    A = ReferenceFrame('A')

    u1, u2 = dynamicsymbols('u1, u2')

    A.set_ang_vel(N, u1 * A.x + u2 * N.y)

    assert N.partial_velocity(A, u1) == -A.x
    assert N.partial_velocity(A, u1, u2) == (-A.x, -N.y)

    assert A.partial_velocity(N, u1) == A.x
    assert A.partial_velocity(N, u1, u2) == (A.x, N.y)

    assert N.partial_velocity(N, u1) == 0
    assert A.partial_velocity(A, u1) == 0


def test_partial_velocity():
    q1, q2, q3, u1, u2, u3 = dynamicsymbols('q1 q2 q3 u1 u2 u3')
    u4, u5 = dynamicsymbols('u4, u5')
    r = symbols('r')

    N = ReferenceFrame('N')
    Y = N.orientnew('Y', 'Axis', [q1, N.z])
    L = Y.orientnew('L', 'Axis', [q2, Y.x])
    R = L.orientnew('R', 'Axis', [q3, L.y])
    R.set_ang_vel(N, u1 * L.x + u2 * L.y + u3 * L.z)

    C = Point('C')
    C.set_vel(N, u4 * L.x + u5 * (Y.z ^ L.x))
    Dmc = C.locatenew('Dmc', r * L.z)
    Dmc.v2pt_theory(C, N, R)

    vel_list = [Dmc.vel(N), C.vel(N), R.ang_vel_in(N)]
    u_list = [u1, u2, u3, u4, u5]
    assert (partial_velocity(vel_list, u_list, N) ==
            [[- r*L.y, r*L.x, 0, L.x, cos(q2)*L.y - sin(q2)*L.z],
            [0, 0, 0, L.x, cos(q2)*L.y - sin(q2)*L.z],
            [L.x, L.y, L.z, 0, 0]])

    # Make sure that partial velocities can be computed regardless if the
    # orientation between frames is defined or not.
    A = ReferenceFrame('A')
    B = ReferenceFrame('B')
    v = u4 * A.x + u5 * B.y
    assert partial_velocity((v, ), (u4, u5), A) == [[A.x, B.y]]

    raises(TypeError, lambda: partial_velocity(Dmc.vel(N), u_list, N))
    raises(TypeError, lambda: partial_velocity(vel_list, u1, N))

