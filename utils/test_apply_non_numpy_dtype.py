
def test_apply_non_numpy_dtype():
    # GH 12244
    df = DataFrame({"dt": date_range("2015-01-01", periods=3, tz="Europe/Brussels")})
    result = df.apply(lambda x: x)
    tm.assert_frame_equal(result, df)

    result = df.apply(lambda x: x + pd.Timedelta("1day"))
    expected = DataFrame(
        {"dt": date_range("2015-01-02", periods=3, tz="Europe/Brussels")}
    )
    tm.assert_frame_equal(result, expected)

