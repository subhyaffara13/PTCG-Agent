
def test_transform_datetime_to_numeric():
    # GH 10972
    # convert dt to float
    df = DataFrame({"a": 1, "b": date_range("2015-01-01", periods=2, freq="D")})
    result = df.groupby("a").b.transform(
        lambda x: x.dt.dayofweek - x.dt.dayofweek.mean()
    )

    expected = Series([-0.5, 0.5], name="b")
    tm.assert_series_equal(result, expected)

    # convert dt to int
    df = DataFrame({"a": 1, "b": date_range("2015-01-01", periods=2, freq="D")})
    result = df.groupby("a").b.transform(
        lambda x: x.dt.dayofweek - x.dt.dayofweek.min()
    )

    expected = Series([0, 1], dtype=np.int32, name="b")
    tm.assert_series_equal(result, expected)

