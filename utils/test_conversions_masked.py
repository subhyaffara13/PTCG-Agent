
def test_conversions_masked():
    x1 = np.ma.array(['k', 'b'], mask=[True, False])
    x2 = np.ma.array([[0, 0, 0, 1], [0, 0, 1, 1]])
    x2[0] = np.ma.masked
    assert mcolors.to_rgba(x1[0]) == (0, 0, 0, 0)
    assert_array_equal(mcolors.to_rgba_array(x1),
                       [[0, 0, 0, 0], [0, 0, 1, 1]])
    assert_array_equal(mcolors.to_rgba_array(x2), mcolors.to_rgba_array(x1))

