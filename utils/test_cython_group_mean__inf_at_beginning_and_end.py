
def test_cython_group_mean_Inf_at_beginning_and_end():
    # GH 50367
    actual = np.array([[np.nan, np.nan], [np.nan, np.nan]], dtype="float64")
    counts = np.array([0, 0], dtype="int64")
    data = np.array(
        [[np.inf, 1.0], [1.0, 2.0], [2.0, 3.0], [3.0, 4.0], [4.0, 5.0], [5, np.inf]],
        dtype="float64",
    )
    labels = np.array([0, 1, 0, 1, 0, 1], dtype=np.intp)

    group_mean(actual, counts, data, labels, is_datetimelike=False)

    expected = np.array([[np.inf, 3], [3, np.inf]], dtype="float64")

    tm.assert_numpy_array_equal(
        actual,
        expected,
    )

