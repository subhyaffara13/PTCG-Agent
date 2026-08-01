
def test_print(capture):
    with capture:
        m.print_function()
    assert (
        capture
        == """
        Hello, World!
        1 2.0 three True -- multiple args
        *args-and-a-custom-separator
        no new line here -- next print
        flush
        py::print + str.format = this
    """
    )
    assert capture.stderr == "this goes to stderr"

    with pytest.raises(RuntimeError) as excinfo:
        m.print_failure()
    assert str(excinfo.value) == "Unable to convert call argument " + (
        "'1' of type 'UnregisteredType' to Python object"
        if detailed_error_messages_enabled
        else "'1' to Python object (#define PYBIND11_DETAILED_ERROR_MESSAGES or compile in debug mode for details)"
    )


def test_print():
    u = Quantity("unitname", abbrev="dam")
    assert repr(u) == "unitname"
    assert str(u) == "unitname"

