
def test_zero_sign():
    y = sinpi(-0.0)
    assert y == 0.0
    assert np.signbit(y)

    y = sinpi(0.0)
    assert y == 0.0
    assert not np.signbit(y)

    y = cospi(0.5)
    assert y == 0.0
    assert not np.signbit(y)

