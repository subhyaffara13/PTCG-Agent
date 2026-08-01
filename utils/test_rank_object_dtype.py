
def test_rank_object_dtype(rank_method, ascending, na_option, pct, vals):
    df = DataFrame({"key": ["foo"] * 5, "val": vals})
    mask = df["val"].isna()

    gb = df.groupby("key")
    res = gb.rank(method=rank_method, ascending=ascending, na_option=na_option, pct=pct)

    # construct our expected by using numeric values with the same ordering
    if mask.any():
        df2 = DataFrame({"key": ["foo"] * 5, "val": [0, np.nan, 2, np.nan, 1]})
    else:
        df2 = DataFrame({"key": ["foo"] * 5, "val": [0, 0, 2, 0, 1]})

    gb2 = df2.groupby("key")
    alt = gb2.rank(
        method=rank_method, ascending=ascending, na_option=na_option, pct=pct
    )

    tm.assert_frame_equal(res, alt)

