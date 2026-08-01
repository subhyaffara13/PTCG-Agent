
def test_return_array_pyobject_ptr_cpp_loop(return_array_pyobject_ptr, unwrap):
    # Intentionally all temporaries, do not change.
    arr_from_list = return_array_pyobject_ptr(WrapWithPyValueHolder(6, "seven", -8.0))
    assert isinstance(arr_from_list, np.ndarray)
    assert arr_from_list.dtype == np.dtype("O")
    assert unwrap(arr_from_list) == [6, "seven", -8.0]

