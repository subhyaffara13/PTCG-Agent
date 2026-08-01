
def test_apply_listlike_lambda(ops, expected, by_row):
    # GH53400
    ser = Series([1, 2, 3])
    result = ser.apply(ops, by_row=by_row)
    tm.assert_equal(result, expected)

