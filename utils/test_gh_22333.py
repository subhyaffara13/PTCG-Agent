
def test_gh_22333():
    x = np.array([272, 58, 67, 163, 463, 608, 87, 108, 1378])
    expected = [58, 67, 87, 108, 163, 108, 108, 108, 87]
    actual = ndimage.median_filter(x, size=9, mode='constant')
    assert_array_equal(actual, expected)

