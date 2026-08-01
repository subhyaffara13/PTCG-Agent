
def test_merge_antijoin_on_datetime64tz():
    # GH11405
    left = DataFrame(
        {
            "key": pd.date_range("20151010", periods=2, tz="US/Eastern"),
            "value": [1.0, 2.0],
        }
    )
    right = DataFrame(
        {
            "key": pd.date_range("20151011", periods=3, tz="US/Eastern"),
            "value": [1.0, 2.0, 3.0],
        }
    )

    expected = DataFrame(
        {
            "key": pd.date_range("20151010", periods=1, tz="US/Eastern"),
            "value_x": [1.0],
            "value_y": [np.nan],
        },
        index=[0],
    )
    result = merge(left, right, on="key", how="left_anti")
    tm.assert_frame_equal(result, expected)

    expected = DataFrame(
        {
            "key": pd.date_range("20151012", periods=2, tz="US/Eastern"),
            "value_x": [np.nan, np.nan],
            "value_y": [2.0, 3.0],
        },
        index=[1, 2],
    )
    result = merge(left, right, on="key", how="right_anti")
    tm.assert_frame_equal(result, expected)

