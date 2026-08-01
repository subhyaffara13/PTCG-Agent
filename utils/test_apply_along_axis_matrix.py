
def test_apply_along_axis_matrix():
    # this test is particularly malicious because matrix
    # refuses to become 1d
    # 2018-04-29: moved here from core.tests.test_shape_base.
    def double(row):
        return row * 2

    m = np.matrix([[0, 1], [2, 3]])
    expected = np.matrix([[0, 2], [4, 6]])

    result = np.apply_along_axis(double, 0, m)
    assert_(isinstance(result, np.matrix))
    assert_array_equal(result, expected)

    result = np.apply_along_axis(double, 1, m)
    assert_(isinstance(result, np.matrix))
    assert_array_equal(result, expected)

