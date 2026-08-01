
def test_agg_with_datetime_index_list_agg_func(col_name):
    # GH 22660
    # The parametrized column names would get converted to dates by our
    # date parser. Some would result in OutOfBoundsError (ValueError) while
    # others would result in OverflowError when passed into Timestamp.
    # We catch these errors and move on to the correct branch.
    df = DataFrame(
        list(range(200)),
        index=date_range(
            start="2017-01-01", freq="15min", periods=200, tz="Europe/Berlin"
        ),
        columns=[col_name],
    )
    result = df.resample("1D").aggregate(["mean"])
    expected = DataFrame(
        [47.5, 143.5, 195.5],
        index=date_range(start="2017-01-01", freq="D", periods=3, tz="Europe/Berlin"),
        columns=pd.MultiIndex(levels=[[col_name], ["mean"]], codes=[[0], [0]]),
    )
    tm.assert_frame_equal(result, expected)

