
def test_setitem_partial_row_multiple_columns():
    # https://github.com/pandas-dev/pandas/issues/56503
    df = DataFrame({"A": [1, 2, 3], "B": [4.0, 5, 6]})
    # should not warn
    df.loc[df.index <= 1, ["F", "G"]] = (1, "abc")
    expected = DataFrame(
        {
            "A": [1, 2, 3],
            "B": [4.0, 5, 6],
            "F": [1.0, 1, float("nan")],
            "G": ["abc", "abc", float("nan")],
        }
    )
    tm.assert_frame_equal(df, expected)

