
def test_groupby_agg_ohlc_non_first():
    # GH 21716
    df = DataFrame(
        [[1], [1]],
        columns=Index(["foo"], name="mycols"),
        index=date_range("2018-01-01", periods=2, freq="D", name="dti"),
    )

    expected = DataFrame(
        [[1, 1, 1, 1, 1], [1, 1, 1, 1, 1]],
        columns=MultiIndex.from_tuples(
            (
                ("foo", "sum", "foo"),
                ("foo", "ohlc", "open"),
                ("foo", "ohlc", "high"),
                ("foo", "ohlc", "low"),
                ("foo", "ohlc", "close"),
            ),
            names=["mycols", None, None],
        ),
        index=date_range("2018-01-01", periods=2, freq="D", name="dti"),
    )

    result = df.groupby(Grouper(freq="D")).agg(["sum", "ohlc"])

    tm.assert_frame_equal(result, expected)

