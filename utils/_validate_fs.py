
def _validate_fs(fs, allow_none=True):
    """
    Check if the given sampling frequency is a scalar and raises an exception
    otherwise. If allow_none is False, also raises an exception for none
    sampling rates. Returns the sampling frequency as float or none if the
    input is none.
    """
    if fs is None:
        if not allow_none:
            raise ValueError("Sampling frequency can not be none.")
    else:  # should be float
        if not np.isscalar(fs):
            raise ValueError("Sampling frequency fs must be a single scalar.")
        fs = float(fs)
    return fs

