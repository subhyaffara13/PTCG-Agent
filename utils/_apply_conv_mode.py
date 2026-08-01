
def _apply_conv_mode(ret, s1, s2, mode, axes, xp):
    """Calculate the convolution result shape based on the `mode` argument.

    Returns the result sliced to the correct size for the given mode.

    Parameters
    ----------
    ret : array
        The result array, with the appropriate shape for the 'full' mode.
    s1 : list of int
        The shape of the first input.
    s2 : list of int
        The shape of the second input.
    mode : str {'full', 'valid', 'same'}
        A string indicating the size of the output.
        See the documentation `fftconvolve` for more information.
    axes : list of ints
        Axes over which to compute the convolution.

    Returns
    -------
    ret : array
        A copy of `res`, sliced to the correct size for the given `mode`.

    """
    if mode == "full":
        return xp_copy(ret, xp=xp)
    elif mode == "same":
        return xp_copy(_centered(ret, s1), xp=xp)
    elif mode == "valid":
        shape_valid = [ret.shape[a] if a not in axes else s1[a] - s2[a] + 1
                       for a in range(ret.ndim)]
        return xp_copy(_centered(ret, shape_valid), xp=xp)
    else:
        raise ValueError("acceptable mode flags are 'valid',"
                         " 'same', or 'full'")

