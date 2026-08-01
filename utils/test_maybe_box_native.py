
def test_maybe_box_native(obj, expected_dtype):
    boxed_obj = maybe_box_native(obj)
    result_dtype = type(boxed_obj)
    assert result_dtype is expected_dtype

