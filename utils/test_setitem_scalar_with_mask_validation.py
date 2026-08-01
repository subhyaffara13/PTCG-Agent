
def test_setitem_scalar_with_mask_validation(dtype):
    # https://github.com/pandas-dev/pandas/issues/47628
    # setting None with a boolean mask (through _putmaks) should still result
    # in pd.NA values in the underlying array
    ser = pd.Series(["a", "b", "c"], dtype=dtype)
    mask = np.array([False, True, False])

    ser[mask] = None
    assert ser.array[1] is ser.dtype.na_value

    # for other non-string we should also raise an error
    ser = pd.Series(["a", "b", "c"], dtype=dtype)
    msg = "Invalid value '1' for dtype 'str"
    with pytest.raises(TypeError, match=msg):
        ser[mask] = 1

