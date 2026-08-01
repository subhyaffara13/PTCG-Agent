
def test_negative_value_raises():
    with pytest.raises(ValueError, match="buffer size must be non-negative"):
        np.setbufsize(-5)

    old = np.getbufsize()
    try:
        prev = np.setbufsize(4096)
        assert prev == old
        assert np.getbufsize() == 4096
    finally:
        np.setbufsize(old)

