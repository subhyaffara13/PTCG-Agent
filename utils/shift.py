
def shift(x, a, period=None, _cache=_cache):
    """
    Shift periodic sequence x by a: y(u) = x(u+a).

    If x_j and y_j are Fourier coefficients of periodic functions x
    and y, respectively, then::

          y_j = exp(j*a*2*pi/period*sqrt(-1)) * x_f

    Parameters
    ----------
    x : array_like
        The array to take the pseudo-derivative from.
    a : float
        Defines the parameters of the sinh/sinh pseudo-differential
    period : float, optional
        The period of the sequences x and y. Default period is ``2*pi``.
    """  # numpydoc ignore=RT01
    if isinstance(_cache, threading.local):
        if not hasattr(_cache, 'shift_cache'):
            _cache.shift_cache = {}
        _cache = _cache.shift_cache

    tmp = asarray(x)
    if iscomplexobj(tmp):
        return shift(tmp.real, a, period, _cache) + 1j * shift(
            tmp.imag, a, period, _cache)
    if period is not None:
        a = a*2*pi/period
    n = len(x)
    omega = _cache.get((n,a))
    if omega is None:
        if len(_cache) > 20:
            while _cache:
                _cache.popitem()

        def kernel_real(k,a=a):
            return cos(a*k)

        def kernel_imag(k,a=a):
            return sin(a*k)
        omega_real = convolve.init_convolution_kernel(n,kernel_real,d=0,
                                                      zero_nyquist=0)
        omega_imag = convolve.init_convolution_kernel(n,kernel_imag,d=1,
                                                      zero_nyquist=0)
        _cache[(n,a)] = omega_real,omega_imag
    else:
        omega_real,omega_imag = omega
    overwrite_x = _datacopied(tmp, x)
    return convolve.convolve_z(tmp,omega_real,omega_imag,
                               overwrite_x=overwrite_x)


def shift(input, shift, output=None, order=3, mode='constant', cval=0.0,
          prefilter=True):
    """
    Shift an array.

    The array is shifted using spline interpolation of the requested order.
    Points outside the boundaries of the input are filled according to the
    given mode.

    Parameters
    ----------
    %(input)s
    shift : float or sequence
        The shift along the axes. If a float, `shift` is the same for each
        axis. If a sequence, `shift` should contain one value for each axis.
    %(output)s
    order : int, optional
        The order of the spline interpolation, default is 3.
        The order has to be in the range 0-5.
    %(mode_interp_constant)s
    %(cval)s
    %(prefilter)s

    Returns
    -------
    shift : ndarray
        The shifted input.

    See Also
    --------
    affine_transform : Affine transformations

    Notes
    -----
    For complex-valued `input`, this function shifts the real and imaginary
    components independently.

    .. versionadded:: 1.6.0
        Complex-valued support added.

    Examples
    --------
    Import the necessary modules and an exemplary image.

    >>> from scipy.ndimage import shift
    >>> import matplotlib.pyplot as plt
    >>> from scipy import datasets
    >>> image = datasets.ascent()

    Shift the image vertically by 20 pixels.

    >>> image_shifted_vertically = shift(image, (20, 0))

    Shift the image vertically by -200 pixels and horizontally by 100 pixels.

    >>> image_shifted_both_directions = shift(image, (-200, 100))

    Plot the original and the shifted images.

    >>> fig, axes = plt.subplots(3, 1, figsize=(4, 12))
    >>> plt.gray()  # show the filtered result in grayscale
    >>> top, middle, bottom = axes
    >>> for ax in axes:
    ...     ax.set_axis_off()  # remove coordinate system
    >>> top.imshow(image)
    >>> top.set_title("Original image")
    >>> middle.imshow(image_shifted_vertically)
    >>> middle.set_title("Vertically shifted image")
    >>> bottom.imshow(image_shifted_both_directions)
    >>> bottom.set_title("Image shifted in both directions")
    >>> fig.tight_layout()
    """
    if order < 0 or order > 5:
        raise RuntimeError('spline order not supported')
    input = np.asarray(input)
    if input.ndim < 1:
        raise RuntimeError('input and output rank must be > 0')
    complex_output = np.iscomplexobj(input)
    output = _ni_support._get_output(output, input, complex_output=complex_output)
    if complex_output:
        # import under different name to avoid confusion with shift parameter
        from scipy.ndimage._interpolation import shift as _shift

        kwargs = dict(order=order, mode=mode, prefilter=prefilter)
        _shift(input.real, shift, output=output.real, cval=np.real(cval), **kwargs)
        _shift(input.imag, shift, output=output.imag, cval=np.imag(cval), **kwargs)
        return output
    if prefilter and order > 1:
        padded, npad = _prepad_for_spline_filter(input, mode, cval)
        filtered = spline_filter(padded, order, output=np.float64, mode=mode)
    else:
        npad = 0
        filtered = input
    mode = _ni_support._extend_mode_to_code(mode)
    shift = _ni_support._normalize_sequence(shift, input.ndim)
    shift = [-ii for ii in shift]
    shift = np.asarray(shift, dtype=np.float64)
    if not shift.flags.contiguous:
        shift = shift.copy()
    _nd_image.zoom_shift(filtered, None, shift, output, order, mode, cval,
                         npad, False)
    return output


def shift(
    values: np.ndarray, periods: int, axis: AxisInt, fill_value: Scalar
) -> np.ndarray:
    new_values = values

    if periods == 0 or values.size == 0:
        return new_values.copy()

    # make sure array sent to np.roll is c_contiguous
    f_ordered = values.flags.f_contiguous
    if f_ordered:
        new_values = new_values.T
        axis = new_values.ndim - axis - 1

    if new_values.size:
        new_values = np.roll(
            new_values,
            np.intp(periods),
            axis=axis,
        )

    axis_indexer = [slice(None)] * values.ndim
    if periods > 0:
        axis_indexer[axis] = slice(None, periods)
    else:
        axis_indexer[axis] = slice(periods, None)
    new_values[tuple(axis_indexer)] = fill_value

    # restore original order
    if f_ordered:
        new_values = new_values.T

    return new_values

