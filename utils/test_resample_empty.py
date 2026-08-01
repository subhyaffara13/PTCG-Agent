
def test_resample_empty():
    # GH#52484
    df = DataFrame(
        index=pd.to_datetime(
            ["2018-01-01 00:00:00", "2018-01-01 12:00:00", "2018-01-02 00:00:00"]
        )
    )
    expected = DataFrame(
        index=pd.to_datetime(
            [
                "2018-01-01 00:00:00",
                "2018-01-01 08:00:00",
                "2018-01-01 16:00:00",
                "2018-01-02 00:00:00",
            ]
        )
    )
    result = df.resample("8h").mean()
    tm.assert_frame_equal(result, expected)

