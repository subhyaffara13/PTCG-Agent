
def test_frame_equal_row_order_mismatch(check_like, frame_or_series):
    df1 = DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]}, index=["a", "b", "c"])
    df2 = DataFrame({"A": [3, 2, 1], "B": [6, 5, 4]}, index=["c", "b", "a"])

    if not check_like:  # Do not ignore row-column orderings.
        msg = f"{frame_or_series.__name__}.index are different"
        with pytest.raises(AssertionError, match=msg):
            tm.assert_frame_equal(
                df1, df2, check_like=check_like, obj=frame_or_series.__name__
            )
    else:
        _assert_frame_equal_both(
            df1, df2, check_like=check_like, obj=frame_or_series.__name__
        )

