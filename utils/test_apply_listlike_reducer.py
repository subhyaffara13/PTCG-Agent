
def test_apply_listlike_reducer(string_series, ops, names, how, kwargs):
    # GH 39140
    expected = Series(
        {name: op(string_series) for name, op in zip(names, ops, strict=True)}
    )
    expected.name = "series"
    result = getattr(string_series, how)(ops, **kwargs)
    tm.assert_series_equal(result, expected)

