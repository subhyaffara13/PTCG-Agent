
def test_gh_17703():
    arr_1 = np.array([1, 0, 0])
    arr_2 = np.array([2, 0, 0])
    expected = dice(arr_1, arr_2)
    actual = pdist([arr_1, arr_2], metric='dice')
    assert_allclose(actual, expected)
    actual = cdist(np.atleast_2d(arr_1),
                   np.atleast_2d(arr_2), metric='dice')
    assert_allclose(actual, expected)

