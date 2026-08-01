
def _assert_matching_namespace(actual, desired, xp):
    __tracebackhide__ = True  # Hide traceback for py.test

    desired_arr_space = array_namespace(desired)
    _msg = ("Namespace of desired array does not match expectations "
            "set by the `default_xp` context manager or by the `xp`"
            "pytest fixture.\n"
            f"Desired array's space: {desired_arr_space.__name__}\n"
            f"Expected namespace: {xp.__name__}")
    assert desired_arr_space == xp, _msg

    actual_arr_space = array_namespace(actual)
    _msg = ("Namespace of actual and desired arrays do not match.\n"
            f"Actual: {actual_arr_space.__name__}\n"
            f"Desired: {xp.__name__}")
    assert actual_arr_space == xp, _msg

