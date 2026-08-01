
def test_agg_cython_table_frame(df, func, expected, axis):
    # GH 21224
    # test reducing functions in
    # pandas.core.base.SelectionMixin._cython_table
    warn = None if isinstance(func, str) else FutureWarning
    with tm.assert_produces_warning(warn, match="is currently using DataFrame.*"):
        # GH#53425
        result = df.agg(func, axis=axis)
    tm.assert_series_equal(result, expected)

