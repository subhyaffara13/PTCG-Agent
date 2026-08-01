
def test_auto_point_vel_connected_frames():
    t = dynamicsymbols._t
    q, q1, q2, u = dynamicsymbols('q q1 q2 u')
    N = ReferenceFrame('N')
    B = ReferenceFrame('B')
    O = Point('O')
    O.set_vel(N, u * N.x)
    P = Point('P')
    P.set_pos(O, q1 * N.x + q2 * B.y)
    raises(ValueError, lambda: P.vel(N))
    N.orient(B, 'Axis', (q, B.x))
    assert P.vel(N) == (u + q1.diff(t)) * N.x + q2.diff(t) * B.y - q2 * q.diff(t) * B.z

