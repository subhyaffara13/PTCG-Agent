
def test_string_dtype_default_fill_value():
    # Regression test for gh-29421: default fill_value for StringDType is 'N/A'
    dt = np.dtypes.StringDType()
    data = np.array(['x', 'y', 'z'], dtype=dt)
    # no fill_value passed → uses default_fill_value internally
    arr = np.ma.MaskedArray(data, mask=[True, False, True], dtype=dt)
    # ensure it’s stored as a Python str and equals the expected default
    assert isinstance(arr.fill_value, str)
    assert arr.fill_value == 'N/A'
    # masked slots should be replaced by that default
    assert arr.filled().tolist() == ['N/A', 'y', 'N/A']

