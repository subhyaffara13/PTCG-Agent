
def test_cython_group_sum_Inf_at_beginning_and_end(values, out):
    # GH #53606
    actual = np.array([[np.nan], [np.nan]], dtype="float64")
    counts = np.array([0, 0], dtype="int64")
    data = np.array(values, dtype="float64")
    labels = np.array([0, 1, 1], dtype=np.intp)

    group_sum(actual, counts, data, labels, None, is_datetimelike=False)

    expected = np.array(out, dtype="float64")

    tm.assert_numpy_array_equal(
        actual,
        expected,
    )

