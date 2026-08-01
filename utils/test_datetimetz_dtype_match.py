
def test_datetimetz_dtype_match():
    dtype = DatetimeTZDtype(unit="ns", tz="US/Eastern")
    assert find_common_type([dtype, dtype]) == "datetime64[ns, US/Eastern]"

