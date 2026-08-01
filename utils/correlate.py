
def correlate(a: ArrayLike, v: ArrayLike, mode="valid"):
    v = torch.conj_physical(v)
    return _conv_corr_impl(a, v, mode)


def correlate(input, weights, output=None, mode='reflect', cval=0.0,
              origin=0, *, axes=None):
    """
    Multidimensional correlation.

    The array is correlated with the given kernel.

    Parameters
    ----------
    %(input)s
    weights : ndarray
        array of weights, same number of dimensions as input
    %(output)s
    %(mode_reflect)s
    %(cval)s
    %(origin_multiple)s
    axes : tuple of int or None, optional
        If None, `input` is filtered along all axes. Otherwise,
        `input` is filtered along the specified axes. When `axes` is
        specified, any tuples used for `mode` or `origin` must match the length
        of `axes`. The ith entry in any of these tuples corresponds to the ith
        entry in `axes`.

    Returns
    -------
    result : ndarray
        The result of correlation of `input` with `weights`.

    See Also
    --------
    convolve : Convolve an image with a kernel.

    Examples
    --------
    Correlation is the process of moving a filter mask often referred to
    as kernel over the image and computing the sum of products at each location.

    >>> from scipy.ndimage import correlate
    >>> import numpy as np
    >>> input_img = np.arange(25).reshape(5,5)
    >>> print(input_img)
    [[ 0  1  2  3  4]
    [ 5  6  7  8  9]
    [10 11 12 13 14]
    [15 16 17 18 19]
    [20 21 22 23 24]]

    Define a kernel (weights) for correlation. In this example, it is for sum of
    center and up, down, left and right next elements.

    >>> weights = [[0, 1, 0],
    ...            [1, 1, 1],
    ...            [0, 1, 0]]

    We can calculate a correlation result:
    For example, element ``[2,2]`` is ``7 + 11 + 12 + 13 + 17 = 60``.

    >>> correlate(input_img, weights)
    array([[  6,  10,  15,  20,  24],
        [ 26,  30,  35,  40,  44],
        [ 51,  55,  60,  65,  69],
        [ 76,  80,  85,  90,  94],
        [ 96, 100, 105, 110, 114]])

    """
    return _correlate_or_convolve(input, weights, output, mode, cval,
                                  origin, False, axes)


def correlate(in1, in2, mode='full', method='auto'):
    r"""
    Cross-correlate two N-dimensional arrays.

    Cross-correlate `in1` and `in2`, with the output size determined by the
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
           The output is the full discrete linear cross-correlation
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
        A string indicating which method to use to calculate the correlation.

        ``direct``
           The correlation is determined directly from sums, the definition of
           correlation.
        ``fft``
           The Fast Fourier Transform is used to perform the correlation more
           quickly (only available for numerical arrays.)
        ``auto``
           Automatically chooses direct or Fourier method based on an estimate
           of which is faster (default).  See `convolve` Notes for more detail.

           .. versionadded:: 0.19.0

    Returns
    -------
    correlate : array
        An N-dimensional array containing a subset of the discrete linear
        cross-correlation of `in1` with `in2`.

    See Also
    --------
    choose_conv_method : contains more documentation on `method`.
    correlation_lags : calculates the lag / displacement indices array for 1D
        cross-correlation.

    Notes
    -----
    The correlation z of two d-dimensional arrays x and y is defined as::

        z[...,k,...] = sum[..., i_l, ...] x[..., i_l,...] * conj(y[..., i_l - k,...])

    This way, if ``x`` and ``y`` are 1-D arrays and ``z = correlate(x, y, 'full')``
    then

    .. math::

          z[k] = \sum_{l=0}^{N-1} x_l \, y_{l-k}^{*}

    for :math:`k = -(M-1), \dots, (N-1)`, where :math:`N` is the length of ``x``,
    :math:`M` is the length of ``y``, and :math:`y_m = 0` when :math:`m` is outside the
    valid range :math:`[0, M-1]`. The size of :math:`z` is :math:`N + M - 1` and
    :math:`y^*` denotes the complex conjugate of :math:`y`.

    ``method='fft'`` only works for numerical arrays as it relies on
    `fftconvolve`. In certain cases (i.e., arrays of objects or when
    rounding integers can lose precision), ``method='direct'`` is always used.

    When using ``mode='same'`` with even-length inputs, the outputs of `correlate`
    and `correlate2d` differ: There is a 1-index offset between them.

    Examples
    --------
    Implement a matched filter using cross-correlation, to recover a signal
    that has passed through a noisy channel.

    >>> import numpy as np
    >>> from scipy import signal
    >>> import matplotlib.pyplot as plt
    >>> rng = np.random.default_rng()

    >>> sig = np.repeat([0., 1., 1., 0., 1., 0., 0., 1.], 128)
    >>> sig_noise = sig + rng.standard_normal(len(sig))
    >>> corr = signal.correlate(sig_noise, np.ones(128), mode='same') / 128

    >>> clock = np.arange(64, len(sig), 128)
    >>> fig, (ax_orig, ax_noise, ax_corr) = plt.subplots(3, 1, sharex=True)
    >>> ax_orig.plot(sig)
    >>> ax_orig.plot(clock, sig[clock], 'ro')
    >>> ax_orig.set_title('Original signal')
    >>> ax_noise.plot(sig_noise)
    >>> ax_noise.set_title('Signal with noise')
    >>> ax_corr.plot(corr)
    >>> ax_corr.plot(clock, corr[clock], 'ro')
    >>> ax_corr.axhline(0.5, ls=':')
    >>> ax_corr.set_title('Cross-correlated with rectangular pulse')
    >>> ax_orig.margins(0, 0.1)
    >>> fig.tight_layout()
    >>> plt.show()

    Compute the cross-correlation of a noisy signal with the original signal.

    >>> x = np.arange(128) / 128
    >>> sig = np.sin(2 * np.pi * x)
    >>> sig_noise = sig + rng.standard_normal(len(sig))
    >>> corr = signal.correlate(sig_noise, sig)
    >>> lags = signal.correlation_lags(len(sig), len(sig_noise))
    >>> corr /= np.max(corr)

    >>> fig, (ax_orig, ax_noise, ax_corr) = plt.subplots(3, 1, figsize=(4.8, 4.8))
    >>> ax_orig.plot(sig)
    >>> ax_orig.set_title('Original signal')
    >>> ax_orig.set_xlabel('Sample Number')
    >>> ax_noise.plot(sig_noise)
    >>> ax_noise.set_title('Signal with noise')
    >>> ax_noise.set_xlabel('Sample Number')
    >>> ax_corr.plot(lags, corr)
    >>> ax_corr.set_title('Cross-correlated signal')
    >>> ax_corr.set_xlabel('Lag')
    >>> ax_orig.margins(0, 0.1)
    >>> ax_noise.margins(0, 0.1)
    >>> ax_corr.margins(0, 0.1)
    >>> fig.tight_layout()
    >>> plt.show()

    """
    xp = array_namespace(in1, in2)

    in1 = xp.asarray(in1)
    in2 = xp.asarray(in2)

    if in1.ndim == in2.ndim == 0:
        in2_conj = (xp.conj(in2)
                    if xp.isdtype(in2.dtype, 'complex floating')
                    else in2)
        return in1 * in2_conj
    elif in1.ndim != in2.ndim:
        raise ValueError("in1 and in2 should have the same dimensionality")

    # Don't use _valfrommode, since correlate should not accept numeric modes
    try:
        val = _modedict[mode]
    except KeyError as e:
        raise ValueError("Acceptable mode flags are 'valid',"
                         " 'same', or 'full'.") from e

    # this either calls fftconvolve or this function with method=='direct'
    if method in ('fft', 'auto'):
        return convolve(in1, _reverse_and_conj(in2, xp), mode, method)

    elif method == 'direct':
        # fastpath to faster numpy.correlate for 1d inputs when possible
        if _np_conv_ok(in1, in2, mode, xp):
            a_in1 = np.asarray(in1)
            a_in2 = np.asarray(in2)
            out = np.correlate(a_in1, a_in2, mode)
            return xp.asarray(out)

        # _correlateND is far slower when in2.size > in1.size, so swap them
        # and then undo the effect afterward if mode == 'full'.  Also, it fails
        # with 'valid' mode if in2 is larger than in1, so swap those, too.
        # Don't swap inputs for 'same' mode, since shape of in1 matters.
        swapped_inputs = ((mode == 'full') and (xp_size(in2) > xp_size(in1)) or
                          _inputs_swap_needed(mode, in1.shape, in2.shape))

        if swapped_inputs:
            in1, in2 = in2, in1

        # convert to numpy & back for _sigtools._correlateND
        a_in1 = np.asarray(in1)
        a_in2 = np.asarray(in2)

        if mode == 'valid':
            ps = [i - j + 1 for i, j in zip(in1.shape, in2.shape)]
            out = np.empty(ps, a_in1.dtype)

            z = _sigtools._correlateND(a_in1, a_in2, out, val)

        else:
            ps = [i + j - 1 for i, j in zip(in1.shape, in2.shape)]

            # zero pad input
            in1zpadded = np.zeros(ps, a_in1.dtype)
            sc = tuple(slice(0, i) for i in in1.shape)
            in1zpadded[sc] = a_in1.copy()

            if mode == 'full':
                out = np.empty(ps, a_in1.dtype)
            elif mode == 'same':
                out = np.empty(in1.shape, a_in1.dtype)

            z = _sigtools._correlateND(in1zpadded, a_in2, out, val)

        z = xp.asarray(z)

        if swapped_inputs:
            # Reverse and conjugate to undo the effect of swapping inputs
            z = _reverse_and_conj(z, xp)

        return z

    else:
        raise ValueError("Acceptable method flags are 'auto',"
                         " 'direct', or 'fft'.")


def correlate(a, v, mode='valid', propagate_mask=True):
    """
    Cross-correlation of two 1-dimensional sequences.

    Parameters
    ----------
    a, v : array_like
        Input sequences.
    mode : {'valid', 'same', 'full'}, optional
        Refer to the `np.convolve` docstring.  Note that the default
        is 'valid', unlike `convolve`, which uses 'full'.
    propagate_mask : bool
        If True, then a result element is masked if any masked element contributes
        towards it. If False, then a result element is only masked if no non-masked
        element contribute towards it

    Returns
    -------
    out : MaskedArray
        Discrete cross-correlation of `a` and `v`.

    See Also
    --------
    numpy.correlate : Equivalent function in the top-level NumPy module.

    Examples
    --------
    Basic correlation:

    >>> a = np.ma.array([1, 2, 3])
    >>> v = np.ma.array([0, 1, 0])
    >>> np.ma.correlate(a, v, mode='valid')
    masked_array(data=[2],
                 mask=[False],
           fill_value=999999)

    Correlation with masked elements:

    >>> a = np.ma.array([1, 2, 3], mask=[False, True, False])
    >>> v = np.ma.array([0, 1, 0])
    >>> np.ma.correlate(a, v, mode='valid', propagate_mask=True)
    masked_array(data=[--],
                 mask=[ True],
           fill_value=999999,
                dtype=int64)

    Correlation with different modes and mixed array types:

    >>> a = np.ma.array([1, 2, 3])
    >>> v = np.ma.array([0, 1, 0])
    >>> np.ma.correlate(a, v, mode='full')
    masked_array(data=[0, 1, 2, 3, 0],
                 mask=[False, False, False, False, False],
           fill_value=999999)

    """
    return _convolve_or_correlate(np.correlate, a, v, mode, propagate_mask)


def correlate(a, v, mode='valid'):
    r"""
    Cross-correlation of two 1-dimensional sequences.

    This function computes the correlation as generally defined in signal
    processing texts [1]_:

    .. math:: c_k = \sum_n a_{n+k} \cdot \overline{v}_n

    with a and v sequences being zero-padded where necessary and
    :math:`\overline v` denoting complex conjugation.

    Parameters
    ----------
    a, v : array_like
        Input sequences.
    mode : {'valid', 'same', 'full'}, optional
        Refer to the `convolve` docstring.  Note that the default
        is 'valid', unlike `convolve`, which uses 'full'.

    Returns
    -------
    out : ndarray
        Discrete cross-correlation of `a` and `v`.

    See Also
    --------
    convolve : Discrete, linear convolution of two one-dimensional sequences.
    scipy.signal.correlate : uses FFT which has superior performance
        on large arrays.

    Notes
    -----
    The definition of correlation above is not unique and sometimes
    correlation may be defined differently. Another common definition is [1]_:

    .. math:: c'_k = \sum_n a_{n} \cdot \overline{v_{n+k}}

    which is related to :math:`c_k` by :math:`c'_k = c_{-k}`.

    `numpy.correlate` may perform slowly in large arrays (i.e. n = 1e5)
    because it does not use the FFT to compute the convolution; in that case,
    `scipy.signal.correlate` might be preferable.

    References
    ----------
    .. [1] Wikipedia, "Cross-correlation",
           https://en.wikipedia.org/wiki/Cross-correlation

    Examples
    --------
    >>> import numpy as np
    >>> np.correlate([1, 2, 3], [0, 1, 0.5])
    array([3.5])
    >>> np.correlate([1, 2, 3], [0, 1, 0.5], "same")
    array([2. ,  3.5,  3. ])
    >>> np.correlate([1, 2, 3], [0, 1, 0.5], "full")
    array([0.5,  2. ,  3.5,  3. ,  0. ])

    Using complex sequences:

    >>> np.correlate([1+1j, 2, 3-1j], [0, 1, 0.5j], 'full')
    array([ 0.5-0.5j,  1.0+0.j ,  1.5-1.5j,  3.0-1.j ,  0.0+0.j ])

    Note that you get the time reversed, complex conjugated result
    (:math:`\overline{c_{-k}}`) when the two input sequences a and v change
    places:

    >>> np.correlate([0, 1, 0.5j], [1+1j, 2, 3-1j], 'full')
    array([ 0.0+0.j ,  3.0+1.j ,  1.5+1.5j,  1.0+0.j ,  0.5+0.5j])

    """
    return multiarray.correlate2(a, v, mode)


def correlate(a: ArrayLike, v: ArrayLike, mode: str = 'valid', *,
              precision: lax.PrecisionLike = None,
              preferred_element_type: DTypeLike | None = None) -> Array:
  r"""Correlation of two one dimensional arrays.

  JAX implementation of :func:`numpy.correlate`.

  Correlation of one dimensional arrays is defined as:

  .. math::

     c_k = \sum_j a_{k + j} \overline{v_j}

  where :math:`\overline{v_j}` is the complex conjugate of :math:`v_j`.

  Args:
    a: left-hand input to the correlation. Must have ``a.ndim == 1``.
    v: right-hand input to the correlation. Must have ``v.ndim == 1``.
    mode: controls the size of the output. Available operations are:

      * ``"full"``: output the full correlation of the inputs.
      * ``"same"``: return a centered portion of the ``"full"`` output which
        is the same size as ``a``.
      * ``"valid"``: (default) return the portion of the ``"full"`` output which do not
        depend on padding at the array edges.

    precision: Specify the precision of the computation. Refer to
      :class:`jax.lax.Precision` for a description of available values.

    preferred_element_type: A datatype, indicating to accumulate results to and
      return a result with that datatype. Default is ``None``, which means the
      default accumulation type for the input types.

  Returns:
    Array containing the cross-correlation result.

  See Also:
    - :func:`jax.scipy.signal.correlate`: ND correlation
    - :func:`jax.numpy.convolve`: 1D convolution

  Examples:
    >>> x = jnp.array([1, 2, 3, 2, 1])
    >>> y = jnp.array([4, 5, 6])

    Since default ``mode = 'valid'``, ``jax.numpy.correlate`` returns only the
    portion of correlation where the two arrays fully overlap:

    >>> jnp.correlate(x, y)
    Array([32., 35., 28.], dtype=float32)

    Specifying ``mode = 'full'`` returns full correlation using implicit
    zero-padding at the edges.

    >>> jnp.correlate(x, y, mode='full')
    Array([ 6., 17., 32., 35., 28., 13.,  4.], dtype=float32)

    Specifying ``mode = 'same'`` returns a centered correlation the same size
    as the first input:

    >>> jnp.correlate(x, y, mode='same')
    Array([17., 32., 35., 28., 13.], dtype=float32)

    If both the inputs arrays are real-valued and symmetric then the result will
    also be symmetric and will be equal to the result of ``jax.numpy.convolve``.

    >>> x1 = jnp.array([1, 2, 3, 2, 1])
    >>> y1 = jnp.array([4, 5, 4])
    >>> jnp.correlate(x1, y1, mode='full')
    Array([ 4., 13., 26., 31., 26., 13.,  4.], dtype=float32)
    >>> jnp.convolve(x1, y1, mode='full')
    Array([ 4., 13., 26., 31., 26., 13.,  4.], dtype=float32)

    For complex-valued inputs:

    >>> x2 = jnp.array([3+1j, 2, 2-3j])
    >>> y2 = jnp.array([4, 2-5j, 1])
    >>> jnp.correlate(x2, y2, mode='full')
    Array([ 3. +1.j,  3.+17.j, 18.+11.j, 27. +4.j,  8.-12.j], dtype=complex64)
  """
  a, v = util.ensure_arraylike("correlate", a, v)
  return _conv(a, v, mode=mode, op='correlate',
               precision=precision, preferred_element_type=preferred_element_type)


def correlate(in1: Array, in2: Array, mode: ModeString = 'full', method: str = 'auto',
              precision: PrecisionLike = None) -> Array:
  """Cross-correlation of two N-dimensional arrays.

  JAX implementation of :func:`scipy.signal.correlate`.

  Args:
    in1: left-hand input to the cross-correlation.
    in2: right-hand input to the cross-correlation. Must have ``in1.ndim == in2.ndim``.
    mode: controls the size of the output. Available operations are:

      * ``"full"``: (default) output the full cross-correlation of the inputs.
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
    Array containing the cross-correlation result.

  See Also:
    - :func:`jax.numpy.correlate`: 1D cross-correlation
    - :func:`jax.scipy.signal.correlate2d`: 2D cross-correlation
    - :func:`jax.scipy.signal.convolve`: ND convolution

  Examples:
    A few 1D correlation examples:

    >>> x = jnp.array([1, 2, 3, 2, 1])
    >>> y = jnp.array([1, 3, 2])

    Full 1D correlation uses implicit zero-padding at the edges:

    >>> jax.scipy.signal.correlate(x, y, mode='full')
    Array([ 2.,  7., 13., 15., 11.,  5.,  1.], dtype=float32)

    Specifying ``mode = 'same'`` returns a centered 1D correlation of the same
    size as the first input:

    >>> jax.scipy.signal.correlate(x, y, mode='same')
    Array([ 7., 13., 15., 11.,  5.], dtype=float32)

    Specifying ``mode = 'valid'`` returns only the portion of 1D correlation
    where the two arrays fully overlap:

    >>> jax.scipy.signal.correlate(x, y, mode='valid')
    Array([13., 15., 11.], dtype=float32)
  """
  return convolve(in1, jnp.flip(in2.conj()), mode, precision=precision, method=method)

