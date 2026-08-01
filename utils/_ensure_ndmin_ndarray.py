
def _ensure_ndmin_ndarray(a, *, ndmin: int):
    """This is a helper function of loadtxt and genfromtxt to ensure
        proper minimum dimension as requested

        ndim : int. Supported values 1, 2, 3
                    ^^ whenever this changes, keep in sync with
                       _ensure_ndmin_ndarray_check_param
    """
    # Verify that the array has at least dimensions `ndmin`.
    # Tweak the size and shape of the arrays - remove extraneous dimensions
    if a.ndim > ndmin:
        a = np.squeeze(a)
    # and ensure we have the minimum number of dimensions asked for
    # - has to be in this order for the odd case ndmin=1, a.squeeze().ndim=0
    if a.ndim < ndmin:
        if ndmin == 1:
            a = np.atleast_1d(a)
        elif ndmin == 2:
            a = np.atleast_2d(a).T

    return a

