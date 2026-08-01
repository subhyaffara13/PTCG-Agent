
def test_setting_fill_value_attribute():
    # Regression test for gh-29421: setting .fill_value post-construction works too
    dt = np.dtypes.StringDType()
    arr = np.ma.MaskedArray(
        ["x", "longstring", "mid"], mask=[False, True, False], dtype=dt
    )
    # Setting the attribute should not raise
    arr.fill_value = "Z"
    assert arr.fill_value == "Z"
    # And filled() should use the new fill_value
    assert arr.filled()[0] == "x"
    assert arr.filled()[1] == "Z"
    assert arr.filled()[2] == "mid"

