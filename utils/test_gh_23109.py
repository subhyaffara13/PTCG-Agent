
def test_gh_23109():
    a = np.array([0, 0, 1, 1])
    b = np.array([0, 1, 1, 0])
    w = np.asarray([1.5, 1.2, 0.7, 1.3])
    expected = yule(a, b, w=w)
    assert_allclose(expected, 1.1954022988505748)
    actual = cdist(np.atleast_2d(a),
                   np.atleast_2d(b),
                   metric='yule', w=w)
    assert_allclose(actual, expected)

