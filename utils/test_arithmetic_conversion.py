
def test_arithmetic_conversion(all_arithmetic_operators, other):
    # if we have a float operand we should have a float result
    # if that is equal to an integer
    op = tm.get_op_from_name(all_arithmetic_operators)

    s = pd.Series([1, 2, 3], dtype="Int64")
    result = op(s, other)
    assert result.dtype == "Float64"

