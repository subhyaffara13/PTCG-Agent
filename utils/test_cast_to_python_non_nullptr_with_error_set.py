
def test_cast_to_python_non_nullptr_with_error_set():
    with pytest.raises(SystemError) as excinfo:
        m.cast_to_pyobject_ptr_non_nullptr_with_error_set()
    assert str(excinfo.value) == "src != nullptr but PyErr_Occurred()"
    assert str(excinfo.value.__cause__) == "Reflective of unhealthy error handling."

