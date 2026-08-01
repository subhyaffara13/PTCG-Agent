
def fail_if_equal(actual, desired, err_msg='',):
    """
    Raises an assertion error if two items are equal.

    """
    if isinstance(desired, dict):
        if not isinstance(actual, dict):
            raise AssertionError(repr(type(actual)))
        fail_if_equal(len(actual), len(desired), err_msg)
        for k in desired:
            if k not in actual:
                raise AssertionError(repr(k))
            fail_if_equal(actual[k], desired[k], f'key={k!r}\n{err_msg}')
        return
    if isinstance(desired, (list, tuple)) and isinstance(actual, (list, tuple)):
        fail_if_equal(len(actual), len(desired), err_msg)
        for k in range(len(desired)):
            fail_if_equal(actual[k], desired[k], f'item={k!r}\n{err_msg}')
        return
    if isinstance(actual, np.ndarray) or isinstance(desired, np.ndarray):
        return fail_if_array_equal(actual, desired, err_msg)
    msg = build_err_msg([actual, desired], err_msg)
    if not desired != actual:
        raise AssertionError(msg)

