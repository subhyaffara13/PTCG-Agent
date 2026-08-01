
def test_rolling_axis_count():
    # see gh-26055
    df = DataFrame({"x": range(3), "y": range(3)})

    expected = DataFrame({"x": [1.0, 2.0, 2.0], "y": [1.0, 2.0, 2.0]})
    result = df.rolling(2, min_periods=0).count()
    tm.assert_frame_equal(result, expected)

