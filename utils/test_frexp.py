
def test_frexp():
    mp.dps = 15
    assert frexp(0) == (0.0, 0)
    assert frexp(9) == (0.5625, 4)
    assert frexp(1) == (0.5, 1)
    assert frexp(0.2) == (0.8, -2)
    assert frexp(1000) == (0.9765625, 10)

