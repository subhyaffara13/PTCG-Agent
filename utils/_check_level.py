
def _check_level(label, expected, actual):
    """ Check one level of a potentially nested array """
    if issparse(expected):  # allow different types of sparse matrices
        assert_(issparse(actual))
        assert_array_almost_equal(actual.toarray(),
                                  expected.toarray(),
                                  err_msg=label,
                                  decimal=5)
        return
    # Check types are as expected
    assert_(types_compatible(expected, actual),
            f"Expected type {type(expected)}, got {type(actual)} at {label}")
    # A field in a record array may not be an ndarray
    # A scalar from a record array will be type np.void
    if not isinstance(expected, np.void | np.ndarray | MatlabObject):
        assert_equal(expected, actual)
        return
    # This is an ndarray-like thing
    assert_(expected.shape == actual.shape,
            msg=f'Expected shape {expected.shape}, got {actual.shape} at {label}')
    ex_dtype = expected.dtype
    if ex_dtype.hasobject:  # array of objects
        if isinstance(expected, MatlabObject):
            assert_equal(expected.classname, actual.classname)
        for i, ev in enumerate(expected):
            level_label = f"{label}, [{i}], "
            _check_level(level_label, ev, actual[i])
        return
    if ex_dtype.fields:  # probably recarray
        for fn in ex_dtype.fields:
            level_label = f"{label}, field {fn}, "
            _check_level(level_label,
                         expected[fn], actual[fn])
        return
    if ex_dtype.type in (str,  # string or bool
                         np.str_,
                         np.bool_):
        assert_equal(actual, expected, err_msg=label)
        return
    # Something numeric
    assert_array_almost_equal(actual, expected, err_msg=label, decimal=5)

