
def test_frame_equal_columns_mismatch(check_like, frame_or_series, using_infer_string):
    if using_infer_string:
        dtype = "str"
    else:
        dtype = "object"
    msg = f"""{frame_or_series.__name__}\\.columns are different

{frame_or_series.__name__}\\.columns values are different \\(50\\.0 %\\)
\\[left\\]:  Index\\(\\['A', 'B'\\], dtype='{dtype}'\\)
\\[right\\]: Index\\(\\['A', 'b'\\], dtype='{dtype}'\\)"""

    df1 = DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]}, index=["a", "b", "c"])
    df2 = DataFrame({"A": [1, 2, 3], "b": [4, 5, 6]}, index=["a", "b", "c"])

    with pytest.raises(AssertionError, match=msg):
        tm.assert_frame_equal(
            df1, df2, check_like=check_like, obj=frame_or_series.__name__
        )

