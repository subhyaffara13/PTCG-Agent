
def test_generate_bins(binner, closed, expected):
    values = np.array([1, 2, 3, 4, 5, 6], dtype=np.int64)
    result = lib.generate_bins_dt64(
        values, np.array(binner, dtype=np.int64), closed=closed
    )
    expected = np.array(expected, dtype=np.int64)
    tm.assert_numpy_array_equal(result, expected)

