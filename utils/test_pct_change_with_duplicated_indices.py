
def test_pct_change_with_duplicated_indices():
    # GH30463
    s = Series([np.nan, 1, 2, 3, 9, 18], index=["a", "b"] * 3)
    result = s.pct_change()
    expected = Series([np.nan, np.nan, 1.0, 0.5, 2.0, 1.0], index=["a", "b"] * 3)
    tm.assert_series_equal(result, expected)


def test_pct_change_with_duplicated_indices():
    # GH30463
    data = DataFrame(
        {0: [np.nan, 1, 2, 3, 9, 18], 1: [0, 1, np.nan, 3, 9, 18]}, index=["a", "b"] * 3
    )

    result = data.pct_change()

    second_column = [np.nan, np.inf, np.nan, np.nan, 2.0, 1.0]
    expected = DataFrame(
        {0: [np.nan, np.nan, 1.0, 0.5, 2.0, 1.0], 1: second_column},
        index=["a", "b"] * 3,
    )
    tm.assert_frame_equal(result, expected)

