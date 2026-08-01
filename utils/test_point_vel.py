
def test_point_vel(): #Basic functionality
    q1, q2 = dynamicsymbols('q1 q2')
    N = ReferenceFrame('N')
    B = ReferenceFrame('B')
    Q = Point('Q')
    O = Point('O')
    Q.set_pos(O, q1 * N.x)
    raises(ValueError , lambda: Q.vel(N)) # Velocity of O in N is not defined
    O.set_vel(N, q2 * N.y)
    assert O.vel(N) == q2 * N.y
    raises(ValueError , lambda : O.vel(B)) #Velocity of O is not defined in B

