
def test_time_field_bug():
    # Test a fix for the following error related to GH issue 11324 When
    # non-key fields in a group-by dataframe contained time-based fields
    # that were not returned by the apply function, an exception would be
    # raised.

    df = DataFrame({"a": 1, "b": [datetime.now() for nn in range(10)]})

    def func_with_no_date(batch):
        return Series({"c": 2})

    def func_with_date(batch):
        return Series({"b": datetime(2015, 1, 1), "c": 2})

    dfg_no_conversion = df.groupby(by=["a"]).apply(func_with_no_date)
    dfg_no_conversion_expected = DataFrame({"c": 2}, index=[1])
    dfg_no_conversion_expected.index.name = "a"

    dfg_conversion = df.groupby(by=["a"]).apply(func_with_date)
    dfg_conversion_expected = DataFrame(
        {"b": pd.Timestamp(2015, 1, 1), "c": 2}, index=[1]
    )
    dfg_conversion_expected.index.name = "a"

    tm.assert_frame_equal(dfg_no_conversion, dfg_no_conversion_expected)
    tm.assert_frame_equal(dfg_conversion, dfg_conversion_expected)

