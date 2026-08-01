
def test_support_broadcasting_gh13294_regression():
    a0, b0 = stats.norm.support([0, 0, 0, 1], [1, 1, 1, -1])
    ex_a0 = np.array([-np.inf, -np.inf, -np.inf, np.nan])
    ex_b0 = np.array([np.inf, np.inf, np.inf, np.nan])
    assert_equal(a0, ex_a0)
    assert_equal(b0, ex_b0)
    assert a0.shape == ex_a0.shape
    assert b0.shape == ex_b0.shape

    a1, b1 = stats.norm.support([], [])
    ex_a1, ex_b1 = np.array([]), np.array([])
    assert_equal(a1, ex_a1)
    assert_equal(b1, ex_b1)
    assert a1.shape == ex_a1.shape
    assert b1.shape == ex_b1.shape

    a2, b2 = stats.norm.support([0, 0, 0, 1], [-1])
    ex_a2 = np.array(4*[np.nan])
    ex_b2 = np.array(4*[np.nan])
    assert_equal(a2, ex_a2)
    assert_equal(b2, ex_b2)
    assert a2.shape == ex_a2.shape
    assert b2.shape == ex_b2.shape

