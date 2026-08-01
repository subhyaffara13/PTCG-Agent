
def test_agg_cython_table_transform_series(series, func, expected):
    # GH21224
    # test transforming functions in
    # pandas.core.base.SelectionMixin._cython_table (cumprod, cumsum)
    warn = None if isinstance(func, str) else FutureWarning
    with tm.assert_produces_warning(warn, match="is currently using Series.*"):
        result = series.agg(func)
    tm.assert_series_equal(result, expected)

