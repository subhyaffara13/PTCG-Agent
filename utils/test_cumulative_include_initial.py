
def test_cumulative_include_initial():
    arr = np.arange(8).reshape((2, 2, 2))

    expected = np.array([
        [[0, 0], [0, 1], [2, 4]], [[0, 0], [4, 5], [10, 12]]
    ])
    assert_array_equal(
        np.cumulative_sum(arr, axis=1, include_initial=True), expected
    )

    expected = np.array([
        [[1, 0, 0], [1, 2, 6]], [[1, 4, 20], [1, 6, 42]]
    ])
    assert_array_equal(
        np.cumulative_prod(arr, axis=2, include_initial=True), expected
    )

    out = np.zeros((3, 2), dtype=np.float64)
    expected = np.array([[0, 0], [1, 2], [4, 6]], dtype=np.float64)
    arr = np.arange(1, 5).reshape((2, 2))
    np.cumulative_sum(arr, axis=0, out=out, include_initial=True)
    assert_array_equal(out, expected)

    expected = np.array([1, 2, 4])
    assert_array_equal(
        np.cumulative_prod(np.array([2, 2]), include_initial=True), expected
    )

