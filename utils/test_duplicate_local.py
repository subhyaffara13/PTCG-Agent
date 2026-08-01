
def test_duplicate_local():
    """Tests expected failure when registering a class twice with py::local in the same module"""
    with pytest.raises(RuntimeError) as excinfo:
        m.register_local_external()
    import pybind11_tests

    assert str(excinfo.value) == (
        'generic_type: type "LocalExternal" is already registered!'
        if hasattr(pybind11_tests, "class_")
        else "test_class not enabled"
    )

