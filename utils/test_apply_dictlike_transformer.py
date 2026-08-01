
def test_apply_dictlike_transformer(string_series, ops, by_row):
    # GH 39140
    with np.errstate(all="ignore"):
        expected = concat({name: op(string_series) for name, op in ops.items()})
        expected.name = string_series.name
        result = string_series.apply(ops, by_row=by_row)
        tm.assert_series_equal(result, expected)

