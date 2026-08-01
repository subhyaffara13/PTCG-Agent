
def test_validation(_fname):
    # No exceptions should be raised.
    validate_args(_fname, (None,), 2, {"out": None})

    compat_args = {"axis": 1, "out": None}
    validate_args(_fname, (1, None), 2, compat_args)


def test_validation(_fname):
    # No exceptions should be raised.
    compat_args = {"foo": 1, "bar": None, "baz": -2}
    kwargs = {"baz": -2}

    args = (1, None)
    min_fname_arg_count = 2

    validate_args_and_kwargs(_fname, args, kwargs, min_fname_arg_count, compat_args)


def test_validation(_fname):
    # No exceptions should be raised.
    compat_args = {"f": None, "b": 1, "ba": "s"}

    kwargs = {"f": None, "b": 1}
    validate_kwargs(_fname, kwargs, compat_args)

