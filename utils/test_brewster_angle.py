
def test_brewster_angle():
    m1 = Medium('m1', n=1)
    m2 = Medium('m2', n=1.33)
    assert ae(brewster_angle(m1, m2), 0.93, 2)
    m1 = Medium('m1', permittivity=e0, n=1)
    m2 = Medium('m2', permittivity=e0, n=1.33)
    assert ae(brewster_angle(m1, m2), 0.93, 2)
    assert ae(brewster_angle(1, 1.33), 0.93, 2)

