
def test_list_getitem_invalid_index(list_dtype):
    ser = Series(
        [[1, 2, 3], [4, None, 5], None],
        dtype=ArrowDtype(list_dtype),
    )
    with tm.external_error_raised(pa.ArrowInvalid):
        ser.list[-1]
    with tm.external_error_raised(pa.ArrowInvalid):
        ser.list[5]
    with pytest.raises(ValueError, match="key must be an int or slice, got str"):
        ser.list["abc"]

