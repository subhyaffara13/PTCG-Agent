
def test_raise_invalid_args_g17713():
    # other cases are handled in:
    # test_axis_nan_policy_decorated_positional_axis - multiple values for arg
    # test_axis_nan_policy_decorated_positional_args - unexpected kwd arg
    message = "got an unexpected keyword argument"
    with pytest.raises(TypeError, match=message):
        stats.gmean([1, 2, 3], invalid_arg=True)

    message = " got multiple values for argument"
    with pytest.raises(TypeError, match=message):
        stats.gmean([1, 2, 3], a=True)

    message = "missing 1 required positional argument"
    with pytest.raises(TypeError, match=message):
        stats.gmean()

    message = "takes from 1 to 4 positional arguments but 5 were given"
    with pytest.raises(TypeError, match=message):
        stats.gmean([1, 2, 3], 0, float, [1, 1, 1], 10)

