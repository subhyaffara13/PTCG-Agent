
def test_nan_inf_float(tp):
    """ Check formatting of nan & inf.

        This is only for the str function, and only for simple types.
        The precision of np.float32 and np.longdouble aren't the same as the
        python float precision.

    """
    for x in [np.inf, -np.inf, np.nan]:
        assert_equal(str(tp(x)), _REF[x],
                     err_msg=f'Failed str formatting for type {tp}')

