
def convolve(a: ArrayLike, v: ArrayLike, mode="full"):
    # NumPy: if v is longer than a, the arrays are swapped before computation
    if a.shape[0] < v.shape[0]:
        a, v = v, a

    # flip the weights since numpy does and torch does not
    v = torch.flip(v, (0,))

    return _conv_corr_impl(a, v, mode)


def convolve(signal, kernel):
    """Discrete linear convolution of two iterables.
    Equivalent to polynomial multiplication.

    For example, multiplying ``(x² -x - 20)`` by ``(x - 3)``
    gives ``(x³ -4x² -17x + 60)``.

        >>> list(convolve([1, -1, -20], [1, -3]))
        [1, -4, -17, 60]

    Examples of popular kinds of kernels:

    * The kernel ``[0.25, 0.25, 0.25, 0.25]`` computes a moving average.
      For image data, this blurs the image and reduces noise.
    * The kernel ``[1/2, 0, -1/2]`` estimates the first derivative of
      a function evaluated at evenly spaced inputs.
    * The kernel ``[1, -2, 1]`` estimates the second derivative of a
      function evaluated at evenly spaced inputs.

    Convolutions are mathematically commutative; however, the inputs are
    evaluated differently.  The signal is consumed lazily and can be
    infinite. The kernel is fully consumed before the calculations begin.

    Supports all numeric types: int, float, complex, Decimal, Fraction.

    References:

    * Article:  https://betterexplained.com/articles/intuitive-convolution/
    * Video by 3Blue1Brown:  https://www.youtube.com/watch?v=KuXjwB4LzSA

    """
    # This implementation comes from an older version of the itertools
    # documentation.  While the newer implementation is a bit clearer,
    # this one was kept because the inlined window logic is faster
    # and it avoids an unnecessary deque-to-tuple conversion.
    kernel = tuple(kernel)[::-1]
    n = len(kernel)
    window = deque([0], maxlen=n) * n
    for x in chain(signal, repeat(0, n - 1)):
        window.append(x)
        yield _sumprod(kernel, window)


def convolve(input, weights, output=None, mode='reflect', cval=0.0,
             origin=0, *, axes=None):
    """
    Multidimensional convolution.

    The array is convolved with the given kernel.

    Parameters
    ----------
    %(input)s
    weights : array_like
        Array of weights, same number of dimensions as input
    %(output)s
    %(mode_reflect)s
    cval : scalar, optional
        Value to fill past edges of input if `mode` is 'constant'. Default
        is 0.0
    origin : int or sequence, optional
        Controls the placement of the filter on the input array's pixels.
        A value of 0 (the default) centers the filter over the pixel, with
        positive values shifting the filter to the right, and negative ones
        to the left. By passing a sequence of origins with length equal to
        the number of dimensions of the input array, different shifts can
        be specified along each axis.
    axes : tuple of int or None, optional
        If None, `input` is filtered along all axes. Otherwise,
        `input` is filtered along the specified axes. When `axes` is
        specified, any tuples used for `mode` or `origin` must match the length
        of `axes`. The ith entry in any of these tuples corresponds to the ith
        entry in `axes`.

    Returns
    -------
    result : ndarray
        The result of convolution of `input` with `weights`.

    See Also
    --------
    correlate : Correlate an image with a kernel.

    Notes
    -----
    Each value in result is :math:`C_i = \\sum_j{I_{i+k-j} W_j}`, where
    W is the `weights` kernel,
    j is the N-D spatial index over :math:`W`,
    I is the `input` and k is the coordinate of the center of
    W, specified by `origin` in the input parameters.

    Examples
    --------
    Perhaps the simplest case to understand is ``mode='constant', cval=0.0``,
    because in this case borders (i.e., where the `weights` kernel, centered
    on any one value, extends beyond an edge of `input`) are treated as zeros.

    >>> import numpy as np
    >>> a = np.array([[1, 2, 0, 0],
    ...               [5, 3, 0, 4],
    ...               [0, 0, 0, 7],
    ...               [9, 3, 0, 0]])
    >>> k = np.array([[1,1,1],[1,1,0],[1,0,0]])
    >>> from scipy import ndimage
    >>> ndimage.convolve(a, k, mode='constant', cval=0.0)
    array([[11, 10,  7,  4],
           [10,  3, 11, 11],
           [15, 12, 14,  7],
           [12,  3,  7,  0]])

    Setting ``cval=1.0`` is equivalent to padding the outer edge of `input`
    with 1.0's (and then extracting only the original region of the result).

    >>> ndimage.convolve(a, k, mode='constant', cval=1.0)
    array([[13, 11,  8,  7],
           [11,  3, 11, 14],
           [16, 12, 14, 10],
           [15,  6, 10,  5]])

    With ``mode='reflect'`` (the default), outer values are reflected at the
    edge of `input` to fill in missing values.

    >>> b = np.array([[2, 0, 0],
    ...               [1, 0, 0],
    ...               [0, 0, 0]])
    >>> k = np.array([[0,1,0], [0,1,0], [0,1,0]])
    >>> ndimage.convolve(b, k, mode='reflect')
    array([[5, 0, 0],
           [3, 0, 0],
           [1, 0, 0]])

    This includes diagonally at the corners.

    >>> k = np.array([[1,0,0],[0,1,0],[0,0,1]])
    >>> ndimage.convolve(b, k)
    array([[4, 2, 0],
           [3, 2, 0],
           [1, 1, 0]])

    With ``mode='nearest'``, the single nearest value in to an edge in
    `input` is repeated as many times as needed to match the overlapping
    `weights`.

    >>> c = np.array([[2, 0, 1],
    ...               [1, 0, 0],
    ...               [0, 0, 0]])
    >>> k = np.array([[0, 1, 0],
    ...               [0, 1, 0],
    ...               [0, 1, 0],
    ...               [0, 1, 0],
    ...               [0, 1, 0]])
    >>> ndimage.convolve(c, k, mode='nearest')
    array([[7, 0, 3],
           [5, 0, 2],
           [3, 0, 1]])

    """
    return _correlate_or_convolve(input, weights, output, mode, cval,
                                  origin, True, axes)


def convolve(in1, in2, mode='full', method='auto'):
    """
    Convolve two N-dimensional arrays.

    Convolve `in1` and `in2`, with the output size determined by the
    `mode` argument.

    Parameters
    ----------
    in1 : array_like
        First input.
    in2 : array_like
        Second input. Should have the same number of dimensions as `in1`.
    mode : str {'full', 'valid', 'same'}, optional
        A string indicating the size of the output:

        ``full``
           The output is the full discrete linear convolution
           of the inputs. (Default)
        ``valid``
           The output consists only of those elements that do not
           rely on the zero-padding. In 'valid' mode, either `in1` or `in2`
           must be at least as large as the other in every dimension.
        ``same``
           Output size will be ``N``, the same size as `in1`, centered
           with respect to the 'full' output.
           Boundary effects may be visible.
    method : str {'auto', 'direct', 'fft'}, optional
        A string indicating which method to use to calculate the convolution.

        ``direct``
           The convolution is determined directly from sums, the definition of
           convolution.
        ``fft``
           The Fourier Transform is used to perform the convolution by calling
           `fftconvolve`.
        ``auto``
           Automatically chooses direct or Fourier method based on an estimate
           of which is faster (default).  See Notes for more detail.

           .. versionadded:: 0.19.0

    Returns
    -------
    convolve : array
        An N-dimensional array containing a subset of the discrete linear
        convolution of `in1` with `in2`.

        The output size along each axis depends on ``mode``. For input
        sizes ``N`` and ``M`` along a given axis:

        - ``full`` : ``N + M - 1``
        - ``same`` : ``N`` (same as the size of `in1`)
        - ``valid`` : ``max(N, M) - min(N, M) + 1``

    Warns
    -----
    RuntimeWarning
        Use of the FFT convolution on input containing NAN or INF will lead
        to the entire output being NAN or INF. Use method='direct' when your
        input contains NAN or INF values.

    See Also
    --------
    numpy.polymul : performs polynomial multiplication (same operation, but
                    also accepts poly1d objects)
    choose_conv_method : chooses the fastest appropriate convolution method
    fftconvolve : Always uses the FFT method.
    oaconvolve : Uses the overlap-add method to do convolution, which is
                 generally faster when the input arrays are large and
                 significantly different in size.

    Notes
    -----
    By default, `convolve` and `correlate` use ``method='auto'``, which calls
    `choose_conv_method` to choose the fastest method using pre-computed
    values (`choose_conv_method` can also measure real-world timing with a
    keyword argument). Because `fftconvolve` relies on floating point numbers,
    there are certain constraints that may force ``method='direct'`` (more detail
    in `choose_conv_method` docstring).

    Examples
    --------
    Smooth a square pulse using a Hann window:

    >>> import numpy as np
    >>> from scipy import signal
    >>> sig = np.repeat([0., 1., 0.], 100)
    >>> win = signal.windows.hann(50)
    >>> filtered = signal.convolve(sig, win, mode='same') / sum(win)

    >>> import matplotlib.pyplot as plt
    >>> fig, (ax_orig, ax_win, ax_filt) = plt.subplots(3, 1, sharex=True)
    >>> ax_orig.plot(sig)
    >>> ax_orig.set_title('Original pulse')
    >>> ax_orig.margins(0, 0.1)
    >>> ax_win.plot(win)
    >>> ax_win.set_title('Filter impulse response')
    >>> ax_win.margins(0, 0.1)
    >>> ax_filt.plot(filtered)
    >>> ax_filt.set_title('Filtered signal')
    >>> ax_filt.margins(0, 0.1)
    >>> fig.tight_layout()
    >>> fig.show()

    """
    xp = array_namespace(in1, in2)

    volume = xp.asarray(in1)
    kernel = xp.asarray(in2)

    if volume.ndim == kernel.ndim == 0:
        return volume * kernel
    elif volume.ndim != kernel.ndim:
        raise ValueError("volume and kernel should have the same "
                         "dimensionality")

    if _inputs_swap_needed(mode, volume.shape, kernel.shape):
        # Convolution is commutative; order doesn't have any effect on output
        volume, kernel = kernel, volume

    if method == 'auto':
        method = choose_conv_method(volume, kernel, mode=mode)

    if method == 'fft':
        out = fftconvolve(volume, kernel, mode=mode)
        result_type = xp.result_type(volume, kernel)
        if xp.isdtype(result_type, 'integral'):
            out = xp.round(out)

        if xp.isnan(xp.reshape(out, (-1,))[0]) or xp.isinf(xp.reshape(out, (-1,))[0]):
            warnings.warn("Use of fft convolution on input with NAN or inf"
                          " results in NAN or inf output. Consider using"
                          " method='direct' instead.",
                          category=RuntimeWarning, stacklevel=2)

        return xp.astype(out, result_type)
    elif method == 'direct':
        # fastpath to faster numpy.convolve for 1d inputs when possible
        if _np_conv_ok(volume, kernel, mode, xp):
            # convert to numpy and back
            a_volume = np.asarray(volume)
            a_kernel = np.asarray(kernel)
            out = np.convolve(a_volume, a_kernel, mode)
            return xp.asarray(out)

        return correlate(volume, _reverse_and_conj(kernel, xp), mode, 'direct')
    else:
        raise ValueError("Acceptable method flags are 'auto',"
                         " 'direct', or 'fft'.")


def convolve(a, v, mode='full', propagate_mask=True):
    """
    Returns the discrete, linear convolution of two one-dimensional sequences.

    Parameters
    ----------
    a, v : array_like
        Input sequences.
    mode : {'valid', 'same', 'full'}, optional
        Refer to the `np.convolve` docstring.
    propagate_mask : bool
        If True, then if any masked element is included in the sum for a result
        element, then the result is masked.
        If False, then the result element is only masked if no non-masked cells
        contribute towards it

    Returns
    -------
    out : MaskedArray
        Discrete, linear convolution of `a` and `v`.

    See Also
    --------
    numpy.convolve : Equivalent function in the top-level NumPy module.
    """
    return _convolve_or_correlate(np.convolve, a, v, mode, propagate_mask)


def convolve(a, v, mode='full'):
    """
    Returns the discrete, linear convolution of two one-dimensional sequences.

    The convolution operator is often seen in signal processing, where it
    models the effect of a linear time-invariant system on a signal [1]_.  In
    probability theory, the sum of two independent random variables is
    distributed according to the convolution of their individual
    distributions.

    If `v` is longer than `a`, the arrays are swapped before computation.

    Parameters
    ----------
    a : (N,) array_like
        First one-dimensional input array.
    v : (M,) array_like
        Second one-dimensional input array.
    mode : {'full', 'valid', 'same'}, optional
        'full':
          By default, mode is 'full'.  This returns the convolution
          at each point of overlap, with an output shape of (N+M-1,). At
          the end-points of the convolution, the signals do not overlap
          completely, and boundary effects may be seen.

        'same':
          Mode 'same' returns output of length ``max(M, N)``.  Boundary
          effects are still visible.

        'valid':
          Mode 'valid' returns output of length
          ``max(M, N) - min(M, N) + 1``.  The convolution product is only given
          for points where the signals overlap completely.  Values outside
          the signal boundary have no effect.

    Returns
    -------
    out : ndarray
        Discrete, linear convolution of `a` and `v`.

    See Also
    --------
    scipy.signal.fftconvolve : Convolve two arrays using the Fast Fourier
                               Transform.
    scipy.linalg.toeplitz : Used to construct the convolution operator.
    polymul : Polynomial multiplication. Same output as convolve, but also
              accepts poly1d objects as input.

    Notes
    -----
    The discrete convolution operation is defined as

    .. math:: (a * v)_n = \\sum_{m = -\\infty}^{\\infty} a_m v_{n - m}

    It can be shown that a convolution :math:`x(t) * y(t)` in time/space
    is equivalent to the multiplication :math:`X(f) Y(f)` in the Fourier
    domain, after appropriate padding (padding is necessary to prevent
    circular convolution).  Since multiplication is more efficient (faster)
    than convolution, the function `scipy.signal.fftconvolve` exploits the
    FFT to calculate the convolution of large data-sets.

    References
    ----------
    .. [1] Wikipedia, "Convolution",
        https://en.wikipedia.org/wiki/Convolution

    Examples
    --------
    Note how the convolution operator flips the second array
    before "sliding" the two across one another:

    >>> import numpy as np
    >>> np.convolve([1, 2, 3], [0, 1, 0.5])
    array([0. , 1. , 2.5, 4. , 1.5])

    Only return the middle values of the convolution.
    Contains boundary effects, where zeros are taken
    into account:

    >>> np.convolve([1,2,3],[0,1,0.5], 'same')
    array([1. ,  2.5,  4. ])

    The two arrays are of the same length, so there
    is only one position where they completely overlap:

    >>> np.convolve([1,2,3],[0,1,0.5], 'valid')
    array([2.5])

    """
    a, v = array(a, copy=None, ndmin=1), array(v, copy=None, ndmin=1)
    if len(a) == 0:
        raise ValueError('a cannot be empty')
    if len(v) == 0:
        raise ValueError('v cannot be empty')
    if len(v) > len(a):
        a, v = v, a
    return multiarray.correlate(a, v[::-1], mode)


def convolve(a: ArrayLike, v: ArrayLike, mode: str = 'full', *,
             precision: lax.PrecisionLike = None,
             preferred_element_type: DTypeLike | None = None) -> Array:
  r"""Convolution of two one dimensional arrays.

  JAX implementation of :func:`numpy.convolve`.

  Convolution of one dimensional arrays is defined as:

  .. math::

     c_k = \sum_j a_{k - j} v_j

  Args:
    a: left-hand input to the convolution. Must have ``a.ndim == 1``.
    v: right-hand input to the convolution. Must have ``v.ndim == 1``.
    mode: controls the size of the output. Available operations are:

      * ``"full"``: (default) output the full convolution of the inputs.
      * ``"same"``: return a centered portion of the ``"full"`` output which
        is the same size as ``a``.
      * ``"valid"``: return the portion of the ``"full"`` output which do not
        depend on padding at the array edges.

    precision: Specify the precision of the computation. Refer to
      :class:`jax.lax.Precision` for a description of available values.

    preferred_element_type: A datatype, indicating to accumulate results to and
      return a result with that datatype. Default is ``None``, which means the
      default accumulation type for the input types.

  Returns:
    Array containing the convolved result.

  See Also:
    - :func:`jax.scipy.signal.convolve`: ND convolution
    - :func:`jax.numpy.correlate`: 1D correlation

  Examples:
    A few 1D convolution examples:

    >>> x = jnp.array([1, 2, 3, 2, 1])
    >>> y = jnp.array([4, 1, 2])

    ``jax.numpy.convolve``, by default, returns full convolution using implicit
    zero-padding at the edges:

    >>> jnp.convolve(x, y)
    Array([ 4.,  9., 16., 15., 12.,  5.,  2.], dtype=float32)

    Specifying ``mode = 'same'`` returns a centered convolution the same size
    as the first input:

    >>> jnp.convolve(x, y, mode='same')
    Array([ 9., 16., 15., 12.,  5.], dtype=float32)

    Specifying ``mode = 'valid'`` returns only the portion where the two arrays
    fully overlap:

    >>> jnp.convolve(x, y, mode='valid')
    Array([16., 15., 12.], dtype=float32)

    For complex-valued inputs:

    >>> x1 = jnp.array([3+1j, 2, 4-3j])
    >>> y1 = jnp.array([1, 2-3j, 4+5j])
    >>> jnp.convolve(x1, y1)
    Array([ 3. +1.j, 11. -7.j, 15.+10.j,  7. -8.j, 31. +8.j], dtype=complex64)
  """
  a, v = util.ensure_arraylike("convolve", a, v)
  return _conv(a, v, mode=mode, op='convolve',
               precision=precision, preferred_element_type=preferred_element_type)


def convolve(in1: Array, in2: Array, mode: ModeString = 'full', method: str = 'auto',
             precision: PrecisionLike = None) -> Array:
  """Convolution of two N-dimensional arrays.

  JAX implementation of :func:`scipy.signal.convolve`.

  Args:
    in1: left-hand input to the convolution.
    in2: right-hand input to the convolution. Must have ``in1.ndim == in2.ndim``.
    mode: controls the size of the output. Available operations are:

      * ``"full"``: (default) output the full convolution of the inputs.
      * ``"same"``: return a centered portion of the ``"full"`` output which
        is the same size as ``in1``.
      * ``"valid"``: return the portion of the ``"full"`` output which do not
        depend on padding at the array edges.

    method: controls the computation method. Options are

      * ``"auto"``: (default) always uses the ``"direct"`` method.
      * ``"direct"``: lower to :func:`jax.lax.conv_general_dilated`.
      * ``"fft"``: compute the result via a fast Fourier transform.

    precision: Specify the precision of the computation. Refer to
      :class:`jax.lax.Precision` for a description of available values.

  Returns:
    Array containing the convolved result.

  See Also:
    - :func:`jax.numpy.convolve`: 1D convolution
    - :func:`jax.scipy.signal.convolve2d`: 2D convolution
    - :func:`jax.scipy.signal.correlate`: ND correlation

  Examples:
    A few 1D convolution examples:

    >>> x = jnp.array([1, 2, 3, 2, 1])
    >>> y = jnp.array([1, 1, 1])

    Full convolution uses implicit zero-padding at the edges:

    >>> jax.scipy.signal.convolve(x, y, mode='full')
    Array([1., 3., 6., 7., 6., 3., 1.], dtype=float32)

    Specifying ``mode = 'same'`` returns a centered convolution the same size
    as the first input:

    >>> jax.scipy.signal.convolve(x, y, mode='same')
    Array([3., 6., 7., 6., 3.], dtype=float32)

    Specifying ``mode = 'valid'`` returns only the portion where the two arrays
    fully overlap:

    >>> jax.scipy.signal.convolve(x, y, mode='valid')
    Array([6., 7., 6.], dtype=float32)
  """
  if method == 'fft':
    return fftconvolve(in1, in2, mode=mode)
  elif method in ['direct', 'auto']:
    return _convolve_nd(in1, in2, mode, precision=precision)
  else:
    raise ValueError(f"Got {method=}; expected 'auto', 'fft', or 'direct'.")

