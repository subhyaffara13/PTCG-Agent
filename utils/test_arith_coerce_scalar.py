
def test_arith_coerce_scalar(data, all_arithmetic_operators, using_nan_is_na):
    op = tm.get_op_from_name(all_arithmetic_operators)
    s = pd.Series(data)
    other = 0.01

    result = op(s, other)
    expected = op(s.astype(float), other)
    expected = expected.astype("Float64")
    if not using_nan_is_na:
        expected[s.isna()] = pd.NA

    # rmod results in NaN that wasn't NA in original nullable Series -> unmask it
    if all_arithmetic_operators == "__rmod__" and not using_nan_is_na:
        mask = (s == 0).fillna(False).to_numpy(bool)
        expected.array._mask[mask] = False

    tm.assert_series_equal(result, expected)

