
def test_cast_to_python_nullptr(set_error):
    expected = {
        True: r"^Reflective of healthy error handling\.$",
        False: (
            r"^Internal error: pybind11::error_already_set called "
            r"while Python error indicator not set\.$"
        ),
    }[set_error]
    with pytest.raises(RuntimeError, match=expected):
        m.cast_to_pyobject_ptr_nullptr(set_error)

