
def test_point_a1pt_theorys():
    q, q2 = dynamicsymbols('q q2')
    qd, q2d = dynamicsymbols('q q2', 1)
    qdd, q2dd = dynamicsymbols('q q2', 2)
    N = ReferenceFrame('N')
    B = ReferenceFrame('B')
    B.set_ang_vel(N, qd * B.z)
    O = Point('O')
    P = O.locatenew('P', B.x)
    P.set_vel(B, 0)
    O.set_vel(N, 0)
    assert P.a1pt_theory(O, N, B) == -(qd**2) * B.x + qdd * B.y
    P.set_vel(B, q2d * B.z)
    assert P.a1pt_theory(O, N, B) == -(qd**2) * B.x + qdd * B.y + q2dd * B.z
    O.set_vel(N, q2d * B.x)
    assert P.a1pt_theory(O, N, B) == ((q2dd - qd**2) * B.x + (q2d * qd + qdd) * B.y +
                               q2dd * B.z)

