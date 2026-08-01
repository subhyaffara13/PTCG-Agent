
def test_arg_and_kwargs():
    args = "arg1_value", "arg2_value", 3
    assert m.args_function(*args) == args

    args = "a1", "a2"
    kwargs = {"arg3": "a3", "arg4": 4}
    assert m.args_kwargs_function(*args, **kwargs) == (args, kwargs)

