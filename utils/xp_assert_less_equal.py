
def xp_assert_less_equal(
    actual, desired, *, check_namespace=True, check_dtype=True,
    check_shape=True, check_0d=True, err_msg='', verbose=True, xp=None
):
    __tracebackhide__ = True  # Hide traceback for py.test

    actual, desired, xp = _strict_check(
        actual, desired, xp, check_namespace=check_namespace,
        check_dtype=check_dtype, check_shape=check_shape,
        check_0d=check_0d
    )

    # we call `_strict_check` before `_assert_less` so that scalars are
    # coerced to the `xp` namespace before we apply `xp.nextafter`
    _assert_less(
        actual, xp.nextafter(desired, desired + 1),
        err_msg=err_msg, verbose=verbose, xp=xp
    )

