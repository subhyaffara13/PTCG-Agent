
def test_braycurtis():
    # Regression test for ticket #1430.
    assert_almost_equal(wbraycurtis([1, 2, 3], [2, 4, 6]), 1. / 3, decimal=15)
    assert_almost_equal(wbraycurtis([1, 1, 0, 0], [1, 0, 1, 0]), 0.5, decimal=15)

