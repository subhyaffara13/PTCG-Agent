
def test_agg_cython_table_raises_frame(df, func, expected, axis, using_infer_string):
    # GH 21224
    if using_infer_string:
        expected = (expected, NotImplementedError)

    msg = (
        "can't multiply sequence by non-int of type 'str'"
        "|cannot perform cumprod with type str"  # NotImplementedError python backend
        "|operation 'cumprod' not supported for dtype 'str'"  # TypeError pyarrow
    )
    warn = None if isinstance(func, str) else FutureWarning
    with pytest.raises(expected, match=msg):
        with tm.assert_produces_warning(warn, match="using DataFrame.cumprod"):
            df.agg(func, axis=axis)

