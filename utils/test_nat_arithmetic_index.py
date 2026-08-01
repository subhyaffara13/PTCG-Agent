
def test_nat_arithmetic_index(op_name, value):
    # see gh-11718
    exp_name = "x"
    exp_data = [NaT] * 2

    if value.dtype.kind == "M" and "plus" in op_name:
        expected = DatetimeIndex(exp_data, tz=value.tz, name=exp_name)
    else:
        expected = TimedeltaIndex(exp_data, name=exp_name)
    expected = expected.as_unit(value.unit)

    if not isinstance(value, Index):
        expected = expected.array

    op = _ops[op_name]
    result = op(NaT, value)
    tm.assert_equal(result, expected)

