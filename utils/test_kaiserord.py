
def test_kaiserord():
    assert_raises(ValueError, kaiserord, 1.0, 1.0)
    numtaps, beta = kaiserord(2.285 + 7.95 - 0.001, 1/np.pi)
    assert (numtaps, beta) == (2, 0.0)

