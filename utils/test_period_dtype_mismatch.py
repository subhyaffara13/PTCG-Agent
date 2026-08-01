
def test_period_dtype_mismatch(dtype2):
    dtype = PeriodDtype(freq="D")
    assert find_common_type([dtype, dtype2]) == object
    assert find_common_type([dtype2, dtype]) == object

