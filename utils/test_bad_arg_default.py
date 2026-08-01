
def test_bad_arg_default(msg):
    from pybind11_tests import detailed_error_messages_enabled

    with pytest.raises(RuntimeError) as excinfo:
        m.bad_arg_def_named()
    assert msg(excinfo.value) == (
        "arg(): could not convert default argument 'a: UnregisteredType' in function "
        "'should_fail' into a Python object (type not registered yet?)"
        if detailed_error_messages_enabled
        else "arg(): could not convert default argument into a Python object (type not registered "
        "yet?). #define PYBIND11_DETAILED_ERROR_MESSAGES or compile in debug mode for more information."
    )

    with pytest.raises(RuntimeError) as excinfo:
        m.bad_arg_def_unnamed()
    assert msg(excinfo.value) == (
        "arg(): could not convert default argument 'UnregisteredType' in function "
        "'should_fail' into a Python object (type not registered yet?)"
        if detailed_error_messages_enabled
        else "arg(): could not convert default argument into a Python object (type not registered "
        "yet?). #define PYBIND11_DETAILED_ERROR_MESSAGES or compile in debug mode for more information."
    )

