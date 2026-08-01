
def test_groupby_timedelta_quantile():
    # GH: 29485
    tdi = pd.to_timedelta(np.arange(4), unit="s").as_unit("us")
    df = DataFrame({"value": tdi, "group": [1, 1, 2, 2]})
    result = df.groupby("group").quantile(0.99)
    expected = DataFrame(
        {
            "value": [
                pd.Timedelta("0 days 00:00:00.990000"),
                pd.Timedelta("0 days 00:00:02.990000"),
            ]
        },
        index=Index([1, 2], name="group"),
    )
    tm.assert_frame_equal(result, expected)

