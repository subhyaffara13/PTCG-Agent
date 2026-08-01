
def test_euclideans():
    # Regression test for ticket #1328.
    x1 = np.array([1, 1, 1])
    x2 = np.array([0, 0, 0])

    # Basic test of the calculation.
    assert_almost_equal(wsqeuclidean(x1, x2), 3.0, decimal=14)
    assert_almost_equal(weuclidean(x1, x2), np.sqrt(3), decimal=14)

    # Another check, with random data.
    rs = np.random.RandomState(1234567890)
    x = rs.rand(10)
    y = rs.rand(10)
    d1 = weuclidean(x, y)
    d2 = wsqeuclidean(x, y)
    assert_almost_equal(d1**2, d2, decimal=14)

