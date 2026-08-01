
def _np_conv_ok(volume, kernel, mode, xp):
    """
    See if numpy supports convolution of `volume` and `kernel` (i.e. both are
    1D ndarrays and of the appropriate shape).  NumPy's 'same' mode uses the
    size of the larger input, while SciPy's uses the size of the first input.

    Invalid mode strings will return False and be caught by the calling func.
    """
    if volume.ndim == kernel.ndim == 1:
        if mode in ('full', 'valid'):
            return True
        elif mode == 'same':
            return xp_size(volume) >= xp_size(kernel)
    else:
        return False

