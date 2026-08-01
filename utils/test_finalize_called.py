
def test_finalize_called(ndframe_method):
    cls, init_args, method = ndframe_method
    ndframe = cls(*init_args)

    ndframe.attrs = {"a": 1}
    result = method(ndframe)

    assert result.attrs == {"a": 1}

