
def test_iter_rolling_on_dataframe(expected, window):
    # GH 11704, 40373
    df = DataFrame(
        {
            "A": [1, 2, 3, 4, 5],
            "B": [4, 5, 6, 7, 8],
            "C": date_range(start="2016-01-01", periods=5, freq="D"),
        }
    )

    expecteds = [
        DataFrame(values, index=df.loc[index, "C"]) for (values, index) in expected
    ]
    for expected, actual in zip(expecteds, df.rolling(window, on="C"), strict=False):
        tm.assert_frame_equal(actual, expected)

