
def test_period_dtype_match():
    dtype = PeriodDtype(freq="D")
    assert find_common_type([dtype, dtype]) == "period[D]"

