
def test_critical_angle():
    m1 = Medium('m1', n=1)
    m2 = Medium('m2', n=1.33)
    assert ae(critical_angle(m2, m1), 0.85, 2)

