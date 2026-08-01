
def test_groupby_shift_multiple_periods_unsorted_index():
    # https://github.com/pandas-dev/pandas/pull/62843
    idx = date_range("1/1/2000", periods=4, freq="h")
    df = DataFrame(
        {"a": [1, 2, 3], "b": [True, True, False]},
        index=[idx[2], idx[0], idx[1]],
    )
    result = df.groupby("b")[["a"]].shift([0, 1], freq="h")
    expected = DataFrame(
        {
            "a_0": [1.0, 2.0, 3.0, np.nan],
            "a_1": [3.0, np.nan, 2.0, 1.0],
        },
        index=[idx[2], idx[0], idx[1], idx[3]],
    )
    tm.assert_frame_equal(result, expected)

