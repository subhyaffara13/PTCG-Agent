
def test_apply_index_date(using_infer_string):
    # GH 5788
    ts = [
        "2011-05-16 00:00",
        "2011-05-16 01:00",
        "2011-05-16 02:00",
        "2011-05-16 03:00",
        "2011-05-17 02:00",
        "2011-05-17 03:00",
        "2011-05-17 04:00",
        "2011-05-17 05:00",
        "2011-05-18 02:00",
        "2011-05-18 03:00",
        "2011-05-18 04:00",
        "2011-05-18 05:00",
    ]
    df = DataFrame(
        {
            "value": [
                1.40893,
                1.40760,
                1.40750,
                1.40649,
                1.40893,
                1.40760,
                1.40750,
                1.40649,
                1.40893,
                1.40760,
                1.40750,
                1.40649,
            ],
        },
        index=Index(pd.to_datetime(ts), name="date_time"),
    )
    expected = df.groupby(df.index.date).idxmax()
    result = df.groupby(df.index.date).apply(lambda x: x.idxmax())
    tm.assert_frame_equal(result, expected)

