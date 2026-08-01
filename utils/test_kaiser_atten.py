
def test_kaiser_atten():
    a = kaiser_atten(1, 1.0)
    assert a == 7.95
    a = kaiser_atten(2, 1/np.pi)
    assert a == 2.285 + 7.95

