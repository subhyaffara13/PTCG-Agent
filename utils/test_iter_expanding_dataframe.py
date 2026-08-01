
def test_iter_expanding_dataframe(df, expected, min_periods):
    # GH 11704
    df = DataFrame(df)
    expecteds = [DataFrame(values, index=index) for (values, index) in expected]

    for expected, actual in zip(expecteds, df.expanding(min_periods), strict=False):
        tm.assert_frame_equal(actual, expected)

