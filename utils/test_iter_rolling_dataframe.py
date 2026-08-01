
def test_iter_rolling_dataframe(df, expected, window, min_periods):
    # GH 11704
    df = DataFrame(df)
    expecteds = [DataFrame(values, index=index) for (values, index) in expected]

    for expected, actual in zip(
        expecteds, df.rolling(window, min_periods=min_periods), strict=False
    ):
        tm.assert_frame_equal(actual, expected)

