
def test_agg_apply_corner(ts, tsframe):
    # nothing to group, all NA
    grouped = ts.groupby(ts * np.nan, group_keys=False)
    assert ts.dtype == np.float64

    # groupby float64 values results in a float64 Index
    exp = Series([], dtype=np.float64, index=Index([], dtype=np.float64))
    tm.assert_series_equal(grouped.sum(), exp)
    tm.assert_series_equal(grouped.agg("sum"), exp)
    tm.assert_series_equal(grouped.apply("sum"), exp, check_index_type=False)

    # DataFrame
    grouped = tsframe.groupby(tsframe["A"] * np.nan, group_keys=False)
    exp_df = DataFrame(
        columns=tsframe.columns,
        dtype=float,
        index=Index([], name="A", dtype=np.float64),
    )
    tm.assert_frame_equal(grouped.sum(), exp_df)
    tm.assert_frame_equal(grouped.agg("sum"), exp_df)

    res = grouped.apply(np.sum, axis=0)
    exp_df = exp_df.reset_index(drop=True)
    tm.assert_frame_equal(res, exp_df)

