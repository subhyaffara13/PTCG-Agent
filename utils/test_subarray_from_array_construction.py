
def test_subarray_from_array_construction():
    # Arrays are more complex, since they "broadcast" on success:
    arr = np.array([1, 2])

    res = arr.astype("2i")
    assert_array_equal(res, [[1, 1], [2, 2]])

    res = np.array(arr, dtype="(2,)i")

    assert_array_equal(res, [[1, 1], [2, 2]])

    res = np.array([[(1,), (2,)], arr], dtype="2i")
    assert_array_equal(res, [[[1, 1], [2, 2]], [[1, 1], [2, 2]]])

    # Also try a multi-dimensional example:
    arr = np.arange(5 * 2).reshape(5, 2)
    expected = np.broadcast_to(arr[:, :, np.newaxis, np.newaxis], (5, 2, 2, 2))

    res = arr.astype("(2,2)f")
    assert_array_equal(res, expected)

    res = np.array(arr, dtype="(2,2)f")
    assert_array_equal(res, expected)

