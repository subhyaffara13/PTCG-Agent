
def test_resample_with_timedeltas():
    expected = DataFrame({"A": np.arange(1480)})
    expected = expected.groupby(expected.index // 30).sum()
    expected.index = timedelta_range("0 days", freq="30min", periods=50)

    df = DataFrame(
        {"A": np.arange(1480)},
        index=pd.to_timedelta(np.arange(1480), unit="min").as_unit("us"),
    )
    result = df.resample("30min").sum()

    tm.assert_frame_equal(result, expected)

    s = df["A"]
    result = s.resample("30min").sum()
    tm.assert_series_equal(result, expected["A"])

