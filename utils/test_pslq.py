
def test_pslq():
    mp.dps = 15
    assert pslq([3*pi+4*e/7, pi, e, log(2)]) == [7, -21, -4, 0]
    assert pslq([4.9999999999999991, 1]) == [1, -5]
    assert pslq([2,1]) == [1, -2]

