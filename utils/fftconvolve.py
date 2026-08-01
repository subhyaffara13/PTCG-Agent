
def fftconvolve(in1, in2, mode="full", axes=None):
    """Convolve two N-dimensional arrays using FFT.

    Convolve `in1` and `in2` using the fast Fourier transform method, with
    the output size determined by the `mode` argument.

    This is generally much faster than `convolve` for large arrays (n > ~500),
    but can be slower when only a few output values are needed, and can only
    output float arrays (int or object array inputs will be cast to float).

    As of v0.19, `convolve` automatically chooses this method or the direct
    method based on an estimation of which is faster.

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
    axes : int or array_like of ints or None, optional
        Axes over which to compute the convolution.
        The default is over all axes.

    Returns
    -------
    out : array
        An N-dimensional array containing a subset of the discrete linear
        convolution of `in1` with `in2`.

        The output size along each axis depends on ``mode``. For input
        sizes ``N`` and ``M`` along a given axis:

        - ``full`` : ``N + M - 1``
        - ``same`` : ``N`` (same as the size of `in1`)
        - ``valid`` : ``max(N, M) - min(N, M) + 1``

    See Also
    --------
    convolve : Uses the direct convolution or FFT convolution algorithm
               depending on which is faster.
    oaconvolve : Uses the overlap-add method to do convolution, which is
                 generally faster when the input arrays are large and
                 significantly different in size.

    Examples
    --------
    Autocorrelation of white noise is an impulse.

    >>> import numpy as np
    >>> from scipy import signal
    >>> rng = np.random.default_rng()
    >>> sig = rng.standard_normal(1000)
    >>> autocorr = signal.fftconvolve(sig, sig[::-1], mode='full')

    >>> import matplotlib.pyplot as plt
    >>> fig, (ax_orig, ax_mag) = plt.subplots(2, 1)
    >>> ax_orig.plot(sig)
    >>> ax_orig.set_title('White noise')
    >>> ax_mag.plot(np.arange(-len(sig)+1,len(sig)), autocorr)
    >>> ax_mag.set_title('Autocorrelation')
    >>> fig.tight_layout()
    >>> fig.show()

    Gaussian blur implemented using FFT convolution.  Notice the dark borders
    around the image, due to the zero-padding beyond its boundaries.
    The `convolve2d` function allows for other types of image boundaries,
    but is far slower.

    >>> from scipy import datasets
    >>> face = datasets.face(gray=True)
    >>> kernel = np.outer(signal.windows.gaussian(70, 8),
    ...                   signal.windows.gaussian(70, 8))
    >>> blurred = signal.fftconvolve(face, kernel, mode='same')

    >>> fig, (ax_orig, ax_kernel, ax_blurred) = plt.subplots(3, 1,
    ...                                                      figsize=(6, 15))
    >>> ax_orig.imshow(face, cmap='gray')
    >>> ax_orig.set_title('Original')
    >>> ax_orig.set_axis_off()
    >>> ax_kernel.imshow(kernel, cmap='gray')
    >>> ax_kernel.set_title('Gaussian kernel')
    >>> ax_kernel.set_axis_off()
    >>> ax_blurred.imshow(blurred, cmap='gray')
    >>> ax_blurred.set_title('Blurred')
    >>> ax_blurred.set_axis_off()
    >>> fig.show()

    """
    xp = array_namespace(in1, in2)

    in1 = xp.asarray(in1)
    in2 = xp.asarray(in2)

    if in1.ndim == in2.ndim == 0:  # scalar inputs
        return in1 * in2
    elif in1.ndim != in2.ndim:
        raise ValueError("in1 and in2 should have the same dimensionality")
    elif xp_size(in1) == 0 or xp_size(in2) == 0:  # empty arrays
        return xp.asarray([])

    in1, in2, axes = _init_freq_conv_axes(in1, in2, mode, axes,
                                          sorted_axes=False)

    s1 = in1.shape
    s2 = in2.shape

    shape = [max((s1[i], s2[i])) if i not in axes else s1[i] + s2[i] - 1
             for i in range(in1.ndim)]

    ret = _freq_domain_conv(xp, in1, in2, axes, shape, calc_fast_len=True)

    return _apply_conv_mode(ret, s1, s2, mode, axes, xp=xp)


def fftconvolve(in1: ArrayLike, in2: ArrayLike, mode: ModeString = "full",
                axes: Sequence[int] | None = None) -> Array:
  """
  Convolve two N-dimensional arrays using Fast Fourier Transform (FFT).

  JAX implementation of :func:`scipy.signal.fftconvolve`.

  Args:
    in1: left-hand input to the convolution.
    in2: right-hand input to the convolution. Must have ``in1.ndim == in2.ndim``.
    mode: controls the size of the output. Available operations are:

      * ``"full"``: (default) output the full convolution of the inputs.
      * ``"same"``: return a centered portion of the ``"full"`` output which
        is the same size as ``in1``.
      * ``"valid"``: return the portion of the ``"full"`` output which do not
        depend on padding at the array edges.

    axes: optional sequence of axes along which to apply the convolution.

  Returns:
    Array containing the convolved result.

  See Also:
    - :func:`jax.numpy.convolve`: 1D convolution
    - :func:`jax.scipy.signal.convolve`: direct convolution

  Examples:
    A few 1D convolution examples. Because FFT-based convolution is approximate,
    We use :func:`jax.numpy.printoptions` below to adjust the printing precision:

    >>> x = jnp.array([1, 2, 3, 2, 1])
    >>> y = jnp.array([1, 1, 1])

    Full convolution uses implicit zero-padding at the edges:

    >>> with jax.numpy.printoptions(precision=3):
    ...   print(jax.scipy.signal.fftconvolve(x, y, mode='full'))
    [1. 3. 6. 7. 6. 3. 1.]

    Specifying ``mode = 'same'`` returns a centered convolution the same size
    as the first input:

    >>> with jax.numpy.printoptions(precision=3):
    ...   print(jax.scipy.signal.fftconvolve(x, y, mode='same'))
    [3. 6. 7. 6. 3.]

    Specifying ``mode = 'valid'`` returns only the portion where the two arrays
    fully overlap:

    >>> with jax.numpy.printoptions(precision=3):
    ...   print(jax.scipy.signal.fftconvolve(x, y, mode='valid'))
    [6. 7. 6.]
  """
  check_arraylike('fftconvolve', in1, in2)
  in1, in2 = promote_dtypes_inexact(in1, in2)
  if in1.ndim != in2.ndim:
    raise ValueError("in1 and in2 should have the same dimensionality")
  if mode not in ["same", "full", "valid"]:
    raise ValueError("mode must be one of ['same', 'full', 'valid']")
  _fftconvolve = partial(_fftconvolve_unbatched, mode=mode)
  if axes is None:
    return _fftconvolve(in1, in2)
  axes = _ensure_index_tuple(axes)
  axes = tuple(canonicalize_axis(ax, in1.ndim) for ax in axes)
  mapped_axes = set(range(in1.ndim)) - set(axes)
  if any(in1.shape[i] != in2.shape[i] for i in mapped_axes):
    raise ValueError(f"mapped axes must have same shape; got {in1.shape=} {in2.shape=} {axes=}")
  for ax in sorted(mapped_axes):
    _fftconvolve = api.vmap(_fftconvolve, in_axes=ax, out_axes=ax)
  return _fftconvolve(in1, in2)

