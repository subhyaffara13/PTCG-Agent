
def test_drop_exception_raised(drop_labels, axis, error_type, error_desc):
    ser = Series(range(3), index=list("abc"))
    with pytest.raises(error_type, match=error_desc):
        ser.drop(drop_labels, axis=axis)

