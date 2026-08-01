
def test_yule_all_same():
    # Test yule avoids a divide by zero when exactly equal
    x = np.ones((2, 6), dtype=bool)
    d = wyule(x[0], x[0])
    assert d == 0.0

    d = pdist(x, 'yule')
    assert_equal(d, [0.0])

    d = cdist(x[:1], x[:1], 'yule')
    assert_equal(d, [[0.0]])

