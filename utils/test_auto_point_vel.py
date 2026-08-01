
def test_auto_point_vel():
    t = dynamicsymbols._t
    q1, q2 = dynamicsymbols('q1 q2')
    N = ReferenceFrame('N')
    B = ReferenceFrame('B')
    O = Point('O')
    Q = Point('Q')
    Q.set_pos(O, q1 * N.x)
    O.set_vel(N, q2 * N.y)
    assert Q.vel(N) == q1.diff(t) * N.x + q2 * N.y  # Velocity of Q using O
    P1 = Point('P1')
    P1.set_pos(O, q1 * B.x)
    P2 = Point('P2')
    P2.set_pos(P1, q2 * B.z)
    raises(ValueError, lambda : P2.vel(B)) # O's velocity is defined in different frame, and no
    #point in between has its velocity defined
    raises(ValueError, lambda: P2.vel(N)) # Velocity of O not defined in N

