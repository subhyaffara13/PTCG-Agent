
def test_infer_from_interval(left, right, subtype, closed):
    # GH 30337
    interval = Interval(left, right, closed)
    result_dtype, result_value = infer_dtype_from_scalar(interval)
    expected_dtype = f"interval[{subtype}, {closed}]"
    assert result_dtype == expected_dtype
    assert result_value == interval

