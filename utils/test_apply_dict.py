
def test_apply_dict(df, dicts):
    # GH 8735
    fn = lambda x: x.to_dict()
    reduce_true = df.apply(fn, result_type="reduce")
    reduce_false = df.apply(fn, result_type="expand")
    reduce_none = df.apply(fn)

    tm.assert_series_equal(reduce_true, dicts)
    tm.assert_frame_equal(reduce_false, df)
    tm.assert_series_equal(reduce_none, dicts)

