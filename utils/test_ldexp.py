
def test_ldexp():
    mp.dps = 15
    assert ldexp(mpf(2.5), 0) == 2.5
    assert ldexp(mpf(2.5), -1) == 1.25
    assert ldexp(mpf(2.5), 2) == 10
    assert ldexp(mpf('inf'), 3) == mpf('inf')

