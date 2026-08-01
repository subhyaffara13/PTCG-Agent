
def test_keyword_args_and_generalized_unpacking():
    def f(*args, **kwargs):
        return args, kwargs

    assert m.test_tuple_unpacking(f) == (("positional", 1, 2, 3, 4, 5, 6), {})
    assert m.test_dict_unpacking(f) == (
        ("positional", 1),
        {"key": "value", "a": 1, "b": 2},
    )
    assert m.test_keyword_args(f) == ((), {"x": 10, "y": 20})
    assert m.test_unpacking_and_keywords1(f) == ((1, 2), {"c": 3, "d": 4})
    assert m.test_unpacking_and_keywords2(f) == (
        ("positional", 1, 2, 3, 4, 5),
        {"key": "value", "a": 1, "b": 2, "c": 3, "d": 4, "e": 5},
    )

    with pytest.raises(TypeError) as excinfo:
        m.test_unpacking_error1(f)
    assert "Got multiple values for keyword argument" in str(excinfo.value)

    with pytest.raises(TypeError) as excinfo:
        m.test_unpacking_error2(f)
    assert "Got multiple values for keyword argument" in str(excinfo.value)

    with pytest.raises(RuntimeError) as excinfo:
        m.test_arg_conversion_error1(f)
    assert str(excinfo.value) == "Unable to convert call argument " + (
        "'1' of type 'UnregisteredType' to Python object"
        if detailed_error_messages_enabled
        else "'1' to Python object (#define PYBIND11_DETAILED_ERROR_MESSAGES or compile in debug mode for details)"
    )

    with pytest.raises(RuntimeError) as excinfo:
        m.test_arg_conversion_error2(f)
    assert str(excinfo.value) == "Unable to convert call argument " + (
        "'expected_name' of type 'UnregisteredType' to Python object"
        if detailed_error_messages_enabled
        else "'expected_name' to Python object "
        "(#define PYBIND11_DETAILED_ERROR_MESSAGES or compile in debug mode for details)"
    )

