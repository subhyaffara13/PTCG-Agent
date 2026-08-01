
def eager_warns(warning_type, *, match=None, xp):
    """pytest.warns context manager if arrays of specified namespace are always eager.

    Otherwise, context manager that *ignores* specified warning.
    """
    import pytest
    from scipy._lib._util import ignore_warns
    if is_numpy(xp) or is_array_api_strict(xp) or is_cupy(xp):
        return pytest.warns(warning_type, match=match)
    return ignore_warns(warning_type, match='' if match is None else match)

