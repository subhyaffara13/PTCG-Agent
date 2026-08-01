
def test_array_NA(data, all_arithmetic_operators):
    data, _ = data
    op = tm.get_op_from_name(all_arithmetic_operators)
    check_skip(data, all_arithmetic_operators)

    scalar = pd.NA
    scalar_array = pd.array([pd.NA] * len(data), dtype=data.dtype)

    mask = data._mask.copy()

    if is_bool_not_implemented(data, all_arithmetic_operators):
        msg = "operator '.*' not implemented for bool dtypes"
        with pytest.raises(NotImplementedError, match=msg):
            op(data, scalar)
        # GH#45421 check op doesn't alter data._mask inplace
        tm.assert_numpy_array_equal(mask, data._mask)
        return

    result = op(data, scalar)
    # GH#45421 check op doesn't alter data._mask inplace
    tm.assert_numpy_array_equal(mask, data._mask)

    expected = op(data, scalar_array)
    tm.assert_numpy_array_equal(mask, data._mask)

    tm.assert_extension_array_equal(result, expected)

