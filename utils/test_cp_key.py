
def test_cp_key():
    # from cyclic4 with grlex
    R, x,y,z,t = ring("x,y,z,t", QQ, grlex)

    p1 = (((0, 0, 0, 0), 4), y*z*t**2 + z**2*t**2 - t**4 - 1, 4)
    q1 = (((0, 0, 0, 0), 2), -y**2 - y*t - z*t - t**2, 2)

    p2 = (((0, 0, 0, 2), 3), z**3*t**2 + z**2*t**3 - z - t, 5)
    q2 = (((0, 0, 2, 2), 2), y*z + z*t**5 + z*t + t**6, 13)

    cp1 = critical_pair(p1, q1, R)
    cp2 = critical_pair(p2, q2, R)

    assert cp_key(cp1, R) < cp_key(cp2, R)

    cp1 = critical_pair(p1, p2, R)
    cp2 = critical_pair(q1, q2, R)

    assert cp_key(cp1, R) < cp_key(cp2, R)

