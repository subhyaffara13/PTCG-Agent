
def test_arithmetic_multiindex_align():
    """
    Regression test for: https://github.com/pandas-dev/pandas/issues/33765
    """
    df1 = DataFrame(
        [[1]],
        index=["a"],
        columns=MultiIndex.from_product([[0], [1]], names=["a", "b"]),
    )
    df2 = DataFrame([[1]], index=["a"], columns=Index([0], name="a"))
    expected = DataFrame(
        [[0]],
        index=["a"],
        columns=MultiIndex.from_product([[0], [1]], names=["a", "b"]),
    )
    result = df1 - df2
    tm.assert_frame_equal(result, expected)

