
def test_apply_dictlike_reducer(string_series, ops, how, kwargs, by_row):
    # GH 39140
    expected = Series({name: op(string_series) for name, op in ops.items()})
    expected.name = string_series.name
    result = getattr(string_series, how)(ops, **kwargs)
    tm.assert_series_equal(result, expected)

