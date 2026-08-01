
def test_adding_new_conditional_column() -> None:
    # https://github.com/pandas-dev/pandas/issues/55025
    df = DataFrame({"x": [1]})
    df.loc[df["x"] == 1, "y"] = "1"
    expected = DataFrame({"x": [1], "y": ["1"]})
    tm.assert_frame_equal(df, expected)

    df = DataFrame({"x": [1]})
    # try inserting something which numpy would store as 'object'
    value = lambda x: x
    df.loc[df["x"] == 1, "y"] = value
    expected = DataFrame({"x": [1], "y": [value]})
    tm.assert_frame_equal(df, expected)

