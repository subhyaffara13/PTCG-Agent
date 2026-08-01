
def test_compiletime_checks():
    """Test decorator invocations -> no replacements."""

    def func(ax, x, y): pass
    def func_args(ax, x, y, *args): pass
    def func_kwargs(ax, x, y, **kwargs): pass
    def func_no_ax_args(*args, **kwargs): pass

    # this is ok
    _preprocess_data(replace_names=["x", "y"])(func)
    _preprocess_data(replace_names=["x", "y"])(func_kwargs)
    # this has "enough" information to do all the replaces
    _preprocess_data(replace_names=["x", "y"])(func_args)

    # no positional_parameter_names but needed due to replaces
    with pytest.raises(AssertionError):
        # z is unknown
        _preprocess_data(replace_names=["x", "y", "z"])(func_args)

    # no replacements at all -> all ok...
    _preprocess_data(replace_names=[], label_namer=None)(func)
    _preprocess_data(replace_names=[], label_namer=None)(func_args)
    _preprocess_data(replace_names=[], label_namer=None)(func_kwargs)
    _preprocess_data(replace_names=[], label_namer=None)(func_no_ax_args)

    # label namer is unknown
    with pytest.raises(AssertionError):
        _preprocess_data(label_namer="z")(func)

    with pytest.raises(AssertionError):
        _preprocess_data(label_namer="z")(func_args)

