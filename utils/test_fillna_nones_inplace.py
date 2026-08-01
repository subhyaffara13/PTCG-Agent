
def test_fillna_nones_inplace():
    # GH 48480
    df = DataFrame(
        [[None, None], [None, None]],
        columns=["A", "B"],
    )
    result = df.fillna(value={"A": 1, "B": 2}, inplace=True)
    assert result is df

    expected = DataFrame([[1, 2], [1, 2]], columns=["A", "B"], dtype=object)
    tm.assert_frame_equal(df, expected)

