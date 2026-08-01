
def test_agg_cython_table_raises_series(series, func, expected, using_infer_string):
    # GH21224
    msg = r"[Cc]ould not convert|can't multiply sequence by non-int of type"
    if func == "median" or func is np.nanmedian or func is np.median:
        msg = r"Cannot convert \['a' 'b' 'c'\] to numeric"

    if using_infer_string and func == "cumprod":
        expected = (expected, NotImplementedError)

    msg = (
        msg + "|does not support|has no kernel|Cannot perform|cannot perform|operation"
    )
    warn = None if isinstance(func, str) else FutureWarning

    with pytest.raises(expected, match=msg):
        # e.g. Series('a b'.split()).cumprod() will raise
        with tm.assert_produces_warning(warn, match="is currently using Series.*"):
            series.agg(func)

