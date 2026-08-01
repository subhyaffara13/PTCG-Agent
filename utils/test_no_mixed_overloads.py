
def test_no_mixed_overloads():
    from pybind11_tests import detailed_error_messages_enabled

    with pytest.raises(RuntimeError) as excinfo:
        m.ExampleMandA.add_mixed_overloads1()
    assert str(
        excinfo.value
    ) == "overloading a method with both static and instance methods is not supported; " + (
        "#define PYBIND11_DETAILED_ERROR_MESSAGES or compile in debug mode for more details"
        if not detailed_error_messages_enabled
        else "error while attempting to bind static method ExampleMandA.overload_mixed1"
        "(arg0: float) -> str"
    )

    with pytest.raises(RuntimeError) as excinfo:
        m.ExampleMandA.add_mixed_overloads2()
    assert str(
        excinfo.value
    ) == "overloading a method with both static and instance methods is not supported; " + (
        "#define PYBIND11_DETAILED_ERROR_MESSAGES or compile in debug mode for more details"
        if not detailed_error_messages_enabled
        else "error while attempting to bind instance method ExampleMandA.overload_mixed2"
        "(self: pybind11_tests.methods_and_attributes.ExampleMandA, arg0: int, arg1: int)"
        " -> str"
    )

