
def assert_raises(exception, function, *args, **kwargs):
    try:
        function(*args, **kwargs)
    except exception:
        return
    else:  # pragma: no cover
        raise AssertionError('Did not raise %s.' % exception)


def assert_raises(*args, **kwargs):
    """
    assert_raises(exception_class, callable, *args, **kwargs)
    assert_raises(exception_class)

    Fail unless an exception of class exception_class is thrown
    by callable when invoked with arguments args and keyword
    arguments kwargs. If a different type of exception is
    thrown, it will not be caught, and the test case will be
    deemed to have suffered an error, exactly as for an
    unexpected exception.

    Alternatively, `assert_raises` can be used as a context manager:

    >>> from numpy.testing import assert_raises
    >>> with assert_raises(ZeroDivisionError):
    ...     1 / 0

    is equivalent to

    >>> def div(x, y):
    ...     return x / y
    >>> assert_raises(ZeroDivisionError, div, 1, 0)

    """
    __tracebackhide__ = True  # Hide traceback for py.test
    return _d.assertRaises(*args, **kwargs)

