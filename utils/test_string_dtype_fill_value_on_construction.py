
def test_string_dtype_fill_value_on_construction():
    # Regression test for gh-29421: allow string fill_value on StringDType masked arrays
    dt = np.dtypes.StringDType()
    data = np.array(["A", "test", "variable", ""], dtype=dt)
    mask = [True, False, True, True]
    # Prior to the fix, this would TypeError; now it should succeed
    arr = np.ma.MaskedArray(data, mask=mask, fill_value="FILL", dtype=dt)
    assert isinstance(arr.fill_value, str)
    assert arr.fill_value == "FILL"
    filled = arr.filled()
    # Masked positions should be replaced by 'FILL'
    assert filled.tolist() == ["FILL", "test", "FILL", "FILL"]

