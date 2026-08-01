
def test_positional_slice_groups_datetimelike():
    # GH 21651
    expected = DataFrame(
        {
            "date": pd.date_range("2010-01-01", freq="12h", periods=5),
            "vals": range(5),
            "let": list("abcde"),
        }
    )
    result = expected.groupby(
        [expected.let, expected.date.dt.date], group_keys=False
    ).apply(lambda x: x.iloc[0:])
    tm.assert_frame_equal(result, expected[["date", "vals"]])

