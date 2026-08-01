
def test_auto_vel_dont_overwrite():
    t = dynamicsymbols._t
    q1, q2, u1 = dynamicsymbols('q1, q2, u1')
    N = ReferenceFrame('N')
    P = Point('P1')
    P.set_vel(N, u1 * N.x)
    P1 = Point('P1')
    P1.set_pos(P, q2 * N.y)
    assert P1.vel(N) == q2.diff(t) * N.y + u1 * N.x
    assert P.vel(N) == u1 * N.x
    P1.set_vel(N, u1 * N.z)
    assert P1.vel(N) == u1 * N.z

