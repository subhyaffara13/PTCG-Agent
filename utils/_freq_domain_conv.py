
def _freq_domain_conv(xp, in1, in2, axes, shape, calc_fast_len=False):
    """Convolve two arrays in the frequency domain.

    This function implements only base the FFT-related operations.
    Specifically, it converts the signals to the frequency domain, multiplies
    them, then converts them back to the time domain.  Calculations of axes,
    shapes, convolution mode, etc. are implemented in higher level-functions,
    such as `fftconvolve` and `oaconvolve`.  Those functions should be used
    instead of this one.

    Parameters
    ----------
    in1 : array_like
        First input.
    in2 : array_like
        Second input. Should have the same number of dimensions as `in1`.
    axes : array_like of ints
        Axes over which to compute the FFTs.
    shape : array_like of ints
        The sizes of the FFTs.
    calc_fast_len : bool, optional
        If `True`, set each value of `shape` to the next fast FFT length.
        Default is `False`, use `axes` as-is.

    Returns
    -------
    out : array
        An N-dimensional array containing the discrete linear convolution of
        `in1` with `in2`.

    """
    if not len(axes):
        return in1 * in2

    complex_result = (xp.isdtype(in1.dtype, 'complex floating') or
                      xp.isdtype(in2.dtype, 'complex floating'))

    if calc_fast_len:
        # Speed up FFT by padding to optimal size.
        fshape = [
            sp_fft.next_fast_len(shape[a], not complex_result) for a in axes]
    else:
        fshape = shape

    if not complex_result:
        fft, ifft = sp_fft.rfftn, sp_fft.irfftn
    else:
        fft, ifft = sp_fft.fftn, sp_fft.ifftn

    if xp.isdtype(in1.dtype, 'integral'):
        in1 = xp.astype(in1, xp_default_dtype(xp))
    if xp.isdtype(in2.dtype, 'integral'):
        in2 = xp.astype(in2, xp_default_dtype(xp))

    sp1 = fft(in1, fshape, axes=axes)
    sp2 = fft(in2, fshape, axes=axes)

    ret = ifft(sp1 * sp2, fshape, axes=axes)

    if calc_fast_len:
        fslice = tuple([slice(sz) for sz in shape])
        ret = ret[fslice]

    return ret

