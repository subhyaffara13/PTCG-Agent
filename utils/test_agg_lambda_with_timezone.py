
def test_agg_lambda_with_timezone():
    # GH 23683
    df = DataFrame(
        {
            "tag": [1, 1],
            "date": [
                pd.Timestamp("2018-01-01", tz="UTC"),
                pd.Timestamp("2018-01-02", tz="UTC"),
            ],
        }
    )
    result = df.groupby("tag").agg({"date": lambda e: e.head(1)})
    expected = DataFrame(
        [pd.Timestamp("2018-01-01", tz="UTC")],
        index=Index([1], name="tag"),
        columns=["date"],
    )
    tm.assert_frame_equal(result, expected)

