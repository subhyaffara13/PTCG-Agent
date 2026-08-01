
def xp_assert_close_nulp(actual, desired, *, nulp=1, check_namespace=True,
                         check_dtype=True, check_shape=True, check_0d=True,
                         err_msg='', xp=None):
    __tracebackhide__ = True  # Hide traceback for py.test

    actual, desired, xp = _strict_check(
        actual, desired, xp,
        check_namespace=check_namespace, check_dtype=check_dtype,
        check_shape=check_shape, check_0d=check_0d
    )

    actual, desired = map(_xp_copy_to_numpy, (actual, desired))
    return np.testing.assert_array_almost_equal_nulp(actual, desired, nulp=nulp)

