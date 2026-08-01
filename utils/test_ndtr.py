
def test_ndtr():
    assert_equal(sc.ndtr(0), 0.5)
    assert_allclose(sc.ndtr(1), 0.8413447460685429)

