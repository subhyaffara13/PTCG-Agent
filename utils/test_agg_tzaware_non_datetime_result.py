
def test_agg_tzaware_non_datetime_result(as_period):
    # discussed in GH#29589, fixed in GH#29641, operating on tzaware values
    #  with function that is not dtype-preserving
    dti = date_range("2012-01-01", periods=4, tz="UTC")
    if as_period:
        dti = dti.tz_localize(None).to_period("D")

    df = DataFrame({"a": [0, 0, 1, 1], "b": dti})
    gb = df.groupby("a")

    # Case that _does_ preserve the dtype
    result = gb["b"].agg(lambda x: x.iloc[0])
    expected = Series(dti[::2], name="b")
    expected.index.name = "a"
    tm.assert_series_equal(result, expected)

    # Cases that do _not_ preserve the dtype
    result = gb["b"].agg(lambda x: x.iloc[0].year)
    expected = Series([2012, 2012], name="b")
    expected.index.name = "a"
    tm.assert_series_equal(result, expected)

    result = gb["b"].agg(lambda x: x.iloc[-1] - x.iloc[0])
    expected = Series(
        [pd.Timedelta(days=1), pd.Timedelta(days=1)], name="b", dtype="m8[us]"
    )
    expected.index.name = "a"
    if as_period:
        expected = Series([pd.offsets.Day(1), pd.offsets.Day(1)], name="b")
        expected.index.name = "a"
    tm.assert_series_equal(result, expected)

