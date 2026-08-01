
def test_cross_module_exceptions(msg):
    with pytest.raises(RuntimeError) as excinfo:
        cm.raise_runtime_error()
    assert str(excinfo.value) == "My runtime error"

    with pytest.raises(ValueError) as excinfo:
        cm.raise_value_error()
    assert str(excinfo.value) == "My value error"

    with pytest.raises(ValueError) as excinfo:
        cm.throw_pybind_value_error()
    assert str(excinfo.value) == "pybind11 value error"

    with pytest.raises(TypeError) as excinfo:
        cm.throw_pybind_type_error()
    assert str(excinfo.value) == "pybind11 type error"

    with pytest.raises(StopIteration) as excinfo:
        cm.throw_stop_iteration()

    with pytest.raises(cm.LocalSimpleException) as excinfo:
        cm.throw_local_simple_error()
    assert msg(excinfo.value) == "external mod"

    with pytest.raises(KeyError) as excinfo:
        cm.throw_local_error()
    # KeyError is a repr of the key, so it has an extra set of quotes
    assert str(excinfo.value) == "'just local'"

