
def test_agg_cython_table_series(series, func, expected):
    # GH21224
    # test reducing functions in
    # pandas.core.base.SelectionMixin._cython_table
    warn = None if isinstance(func, str) else FutureWarning
    with tm.assert_produces_warning(warn, match="is currently using Series.*"):
        result = series.agg(func)
    if is_number(expected):
        assert np.isclose(result, expected, equal_nan=True)
    else:
        assert result == expected

