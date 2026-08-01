
def test_apply_listlike_transformer(string_series, ops, names, by_row):
    # GH 39140
    with np.errstate(all="ignore"):
        expected = concat([op(string_series) for op in ops], axis=1)
        expected.columns = names
        result = string_series.apply(ops, by_row=by_row)
        tm.assert_frame_equal(result, expected)

