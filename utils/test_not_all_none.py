
def test_not_all_none(i, _fname):
    bad_arg = "foo"
    msg = (
        rf"the '{bad_arg}' parameter is not supported "
        rf"in the pandas implementation of {_fname}\(\)"
    )

    compat_args = {"foo": 1, "bar": "s", "baz": None}

    kwarg_keys = ("foo", "bar", "baz")
    kwarg_vals = (2, "s", None)

    kwargs = dict(zip(kwarg_keys[:i], kwarg_vals[:i], strict=True))

    with pytest.raises(ValueError, match=msg):
        validate_kwargs(_fname, kwargs, compat_args)

