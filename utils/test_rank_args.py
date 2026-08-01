
def test_rank_args(grps, vals, ties_method, ascending, pct, exp):
    key = np.repeat(grps, len(vals))

    orig_vals = vals
    vals = list(vals) * len(grps)
    if isinstance(orig_vals, np.ndarray):
        vals = np.array(vals, dtype=orig_vals.dtype)

    df = DataFrame({"key": key, "val": vals})
    result = df.groupby("key").rank(method=ties_method, ascending=ascending, pct=pct)

    exp_df = DataFrame(exp * len(grps), columns=["val"])
    tm.assert_frame_equal(result, exp_df)

