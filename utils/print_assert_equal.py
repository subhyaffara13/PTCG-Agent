
def print_assert_equal(test_string, actual, desired):
    """
    Test if two objects are equal, and print an error message if test fails.

    The test is performed with ``actual == desired``.

    Parameters
    ----------
    test_string : str
        The message supplied to AssertionError.
    actual : object
        The object to test for equality against `desired`.
    desired : object
        The expected result.

    Examples
    --------
    >>> np.testing.print_assert_equal(
    ...     "Test XYZ of func xyz", [0, 1], [0, 1]
    ... )  # doctest: +SKIP
    >>> np.testing.print_assert_equal(
    ...     "Test XYZ of func xyz", [0, 1], [0, 2]
    ... )  # doctest: +SKIP
    Traceback (most recent call last):
    ...
    AssertionError: Test XYZ of func xyz failed
    ACTUAL:
    [0, 1]
    DESIRED:
    [0, 2]

    """
    __tracebackhide__ = True  # Hide traceback for py.test
    import pprint

    if actual != desired:
        msg = StringIO()
        msg.write(test_string)
        msg.write(" failed\nACTUAL: \n")
        pprint.pprint(actual, msg)
        msg.write("DESIRED: \n")
        pprint.pprint(desired, msg)
        raise AssertionError(msg.getvalue())


def print_assert_equal(test_string, actual, desired):
    """
    Test if two objects are equal, and print an error message if test fails.

    The test is performed with ``actual == desired``.

    Parameters
    ----------
    test_string : str
        The message supplied to AssertionError.
    actual : object
        The object to test for equality against `desired`.
    desired : object
        The expected result.

    Examples
    --------
    >>> np.testing.print_assert_equal('Test XYZ of func xyz', [0, 1], [0, 1])
    >>> np.testing.print_assert_equal('Test XYZ of func xyz', [0, 1], [0, 2])
    Traceback (most recent call last):
    ...
    AssertionError: Test XYZ of func xyz failed
    ACTUAL:
    [0, 1]
    DESIRED:
    [0, 2]

    """
    __tracebackhide__ = True  # Hide traceback for py.test
    import pprint

    if not (actual == desired):
        msg = StringIO()
        msg.write(test_string)
        msg.write(' failed\nACTUAL: \n')
        pprint.pprint(actual, msg)
        msg.write('DESIRED: \n')
        pprint.pprint(desired, msg)
        raise AssertionError(msg.getvalue())

