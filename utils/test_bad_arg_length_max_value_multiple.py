
def test_bad_arg_length_max_value_multiple(_fname):
    args = (None, None)
    compat_args = {"foo": None}

    min_fname_arg_count = 2
    max_length = len(compat_args) + min_fname_arg_count
    actual_length = len(args) + min_fname_arg_count
    msg = (
        rf"{_fname}\(\) takes at most {max_length} "
        rf"arguments \({actual_length} given\)"
    )

    with pytest.raises(TypeError, match=msg):
        validate_args(_fname, args, min_fname_arg_count, compat_args)

