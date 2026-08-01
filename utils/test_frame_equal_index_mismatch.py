
def test_frame_equal_index_mismatch(check_like, frame_or_series, using_infer_string):
    if using_infer_string:
        dtype = "str"
    else:
        dtype = "object"
    msg = f"""{frame_or_series.__name__}\\.index are different

{frame_or_series.__name__}\\.index values are different \\(33\\.33333 %\\)
\\[left\\]:  Index\\(\\['a', 'b', 'c'\\], dtype='{dtype}'\\)
\\[right\\]: Index\\(\\['a', 'b', 'd'\\], dtype='{dtype}'\\)
At positional index 2, first diff: c != d"""

    df1 = DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]}, index=["a", "b", "c"])
    df2 = DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]}, index=["a", "b", "d"])

    with pytest.raises(AssertionError, match=msg):
        tm.assert_frame_equal(
            df1, df2, check_like=check_like, obj=frame_or_series.__name__
        )

