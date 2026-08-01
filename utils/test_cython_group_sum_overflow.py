
def test_cython_group_sum_overflow(values, expected_values):
    # GH-60303
    data = np.array([[values] for _ in range(3)])
    labels = np.array([0, 0, 0], dtype=np.intp)
    counts = np.array([0], dtype="int64")

    expected = np.array(expected_values, dtype=values.dtype)
    actual = np.zeros_like(expected)

    group_sum(actual, counts, data, labels, None, is_datetimelike=False)

    tm.assert_numpy_array_equal(actual, expected)

