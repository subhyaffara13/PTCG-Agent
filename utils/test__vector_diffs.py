
def test_Vector_diffs():
    q1, q2, q3, q4 = dynamicsymbols('q1 q2 q3 q4')
    q1d, q2d, q3d, q4d = dynamicsymbols('q1 q2 q3 q4', 1)
    q1dd, q2dd, q3dd, q4dd = dynamicsymbols('q1 q2 q3 q4', 2)
    N = ReferenceFrame('N')
    A = N.orientnew('A', 'Axis', [q3, N.z])
    B = A.orientnew('B', 'Axis', [q2, A.x])
    v1 = q2 * A.x + q3 * N.y
    v2 = q3 * B.x + v1
    v3 = v1.dt(B)
    v4 = v2.dt(B)
    v5 = q1*A.x + q2*A.y + q3*A.z

    assert v1.dt(N) == q2d * A.x + q2 * q3d * A.y + q3d * N.y
    assert v1.dt(A) == q2d * A.x + q3 * q3d * N.x + q3d * N.y
    assert v1.dt(B) == (q2d * A.x + q3 * q3d * N.x + q3d *
                        N.y - q3 * cos(q3) * q2d * N.z)
    assert v2.dt(N) == (q2d * A.x + (q2 + q3) * q3d * A.y + q3d * B.x + q3d *
                        N.y)
    assert v2.dt(A) == q2d * A.x + q3d * B.x + q3 * q3d * N.x + q3d * N.y
    assert v2.dt(B) == (q2d * A.x + q3d * B.x + q3 * q3d * N.x + q3d * N.y -
                        q3 * cos(q3) * q2d * N.z)
    assert v3.dt(N) == (q2dd * A.x + q2d * q3d * A.y + (q3d**2 + q3 * q3dd) *
                        N.x + q3dd * N.y + (q3 * sin(q3) * q2d * q3d -
                        cos(q3) * q2d * q3d - q3 * cos(q3) * q2dd) * N.z)
    assert v3.dt(A) == (q2dd * A.x + (2 * q3d**2 + q3 * q3dd) * N.x + (q3dd -
                        q3 * q3d**2) * N.y + (q3 * sin(q3) * q2d * q3d -
                        cos(q3) * q2d * q3d - q3 * cos(q3) * q2dd) * N.z)
    assert (v3.dt(B) - (q2dd*A.x - q3*cos(q3)*q2d**2*A.y + (2*q3d**2 +
        q3*q3dd)*N.x + (q3dd - q3*q3d**2)*N.y + (2*q3*sin(q3)*q2d*q3d -
        2*cos(q3)*q2d*q3d - q3*cos(q3)*q2dd)*N.z)).express(B).simplify() == 0
    assert v4.dt(N) == (q2dd * A.x + q3d * (q2d + q3d) * A.y + q3dd * B.x +
                        (q3d**2 + q3 * q3dd) * N.x + q3dd * N.y + (q3 *
                        sin(q3) * q2d * q3d - cos(q3) * q2d * q3d - q3 *
                        cos(q3) * q2dd) * N.z)
    assert v4.dt(A) == (q2dd * A.x + q3dd * B.x + (2 * q3d**2 + q3 * q3dd) *
                        N.x + (q3dd - q3 * q3d**2) * N.y + (q3 * sin(q3) *
                        q2d * q3d - cos(q3) * q2d * q3d - q3 * cos(q3) *
                        q2dd) * N.z)
    assert (v4.dt(B) - (q2dd*A.x - q3*cos(q3)*q2d**2*A.y + q3dd*B.x +
                        (2*q3d**2 + q3*q3dd)*N.x + (q3dd - q3*q3d**2)*N.y +
                        (2*q3*sin(q3)*q2d*q3d - 2*cos(q3)*q2d*q3d -
                         q3*cos(q3)*q2dd)*N.z)).express(B).simplify() == 0
    assert v5.dt(B) == q1d*A.x + (q3*q2d + q2d)*A.y + (-q2*q2d + q3d)*A.z
    assert v5.dt(A) == q1d*A.x + q2d*A.y + q3d*A.z
    assert v5.dt(N) == (-q2*q3d + q1d)*A.x + (q1*q3d + q2d)*A.y + q3d*A.z
    assert v3.diff(q1d, N) == 0
    assert v3.diff(q2d, N) == A.x - q3 * cos(q3) * N.z
    assert v3.diff(q3d, N) == q3 * N.x + N.y
    assert v3.diff(q1d, A) == 0
    assert v3.diff(q2d, A) == A.x - q3 * cos(q3) * N.z
    assert v3.diff(q3d, A) == q3 * N.x + N.y
    assert v3.diff(q1d, B) == 0
    assert v3.diff(q2d, B) == A.x - q3 * cos(q3) * N.z
    assert v3.diff(q3d, B) == q3 * N.x + N.y
    assert v4.diff(q1d, N) == 0
    assert v4.diff(q2d, N) == A.x - q3 * cos(q3) * N.z
    assert v4.diff(q3d, N) == B.x + q3 * N.x + N.y
    assert v4.diff(q1d, A) == 0
    assert v4.diff(q2d, A) == A.x - q3 * cos(q3) * N.z
    assert v4.diff(q3d, A) == B.x + q3 * N.x + N.y
    assert v4.diff(q1d, B) == 0
    assert v4.diff(q2d, B) == A.x - q3 * cos(q3) * N.z
    assert v4.diff(q3d, B) == B.x + q3 * N.x + N.y

    # diff() should only express vector components in the derivative frame if
    # the orientation of the component's frame depends on the variable
    v6 = q2**2*N.y + q2**2*A.y + q2**2*B.y
    # already expressed in N
    n_measy = 2*q2
    # A_C_N does not depend on q2, so don't express in N
    a_measy = 2*q2
    # B_C_N depends on q2, so express in N
    b_measx = (q2**2*B.y).dot(N.x).diff(q2)
    b_measy = (q2**2*B.y).dot(N.y).diff(q2)
    b_measz = (q2**2*B.y).dot(N.z).diff(q2)
    n_comp, a_comp = v6.diff(q2, N).args
    assert len(v6.diff(q2, N).args) == 2  # only N and A parts
    assert n_comp[1] == N
    assert a_comp[1] == A
    assert n_comp[0] == Matrix([b_measx, b_measy + n_measy, b_measz])
    assert a_comp[0] == Matrix([0, a_measy, 0])

