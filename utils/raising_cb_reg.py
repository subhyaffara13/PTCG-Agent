
def raising_cb_reg(func):
    class TestException(Exception):
        pass

    def raise_runtime_error():
        raise RuntimeError

    def raise_value_error():
        raise ValueError

    def transformer(excp):
        if isinstance(excp, RuntimeError):
            raise TestException
        raise excp

    # old default
    cb_old = cbook.CallbackRegistry(exception_handler=None)
    cb_old.connect('foo', raise_runtime_error)

    # filter
    cb_filt = cbook.CallbackRegistry(exception_handler=transformer)
    cb_filt.connect('foo', raise_runtime_error)

    # filter
    cb_filt_pass = cbook.CallbackRegistry(exception_handler=transformer)
    cb_filt_pass.connect('foo', raise_value_error)

    return pytest.mark.parametrize('cb, excp',
                                   [[cb_old, RuntimeError],
                                    [cb_filt, TestException],
                                    [cb_filt_pass, ValueError]])(func)

