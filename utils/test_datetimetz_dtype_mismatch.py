
def test_datetimetz_dtype_mismatch(dtype2):
    dtype = DatetimeTZDtype(unit="ns", tz="US/Eastern")
    assert find_common_type([dtype, dtype2]) == object
    assert find_common_type([dtype2, dtype]) == object

