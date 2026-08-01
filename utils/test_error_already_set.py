
def test_error_already_set(msg):
    with pytest.raises(RuntimeError) as excinfo:
        m.throw_already_set(False)
    assert (
        msg(excinfo.value)
        == "Internal error: pybind11::error_already_set called while Python error indicator not set."
    )

    with pytest.raises(ValueError) as excinfo:
        m.throw_already_set(True)
    assert msg(excinfo.value) == "foo"

