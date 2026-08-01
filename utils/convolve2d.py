
def convolve2d(in1, in2, mode='full', boundary='fill', fillvalue=0):
    """
    Convolve two 2-dimensional arrays.

    Convolve `in1` and `in2` with output size determined by `mode`, and
    boundary conditions determined by `boundary` and `fillvalue`.

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
           The output is the same size as `in1`, centered
           with respect to the 'full' output.
    boundary : str {'fill', 'wrap', 'symm'}, optional
        A flag indicating how to handle boundaries:

        ``fill``
           pad input arrays with fillvalue. (default)
        ``wrap``
           circular boundary conditions.
        ``symm``
           symmetrical boundary conditions.

    fillvalue : scalar, optional
        Value to fill pad input arrays with. Default is 0.

    Returns
    -------
    out : ndarray
        A 2-dimensional array containing a subset of the discrete linear
        convolution of `in1` with `in2`.

    Examples
    --------
    Compute the gradient of an image by 2D convolution with a complex Scharr
    operator.  (Horizontal operator is real, vertical is imaginary.)  Use
    symmetric boundary condition to avoid creating edges at the image
    boundaries.

    >>> import numpy as np
    >>> from scipy import signal
    >>> from scipy import datasets
    >>> ascent = datasets.ascent()
    >>> scharr = np.array([[ -3-3j, 0-10j,  +3 -3j],
    ...                    [-10+0j, 0+ 0j, +10 +0j],
    ...                    [ -3+3j, 0+10j,  +3 +3j]]) # Gx + j*Gy
    >>> grad = signal.convolve2d(ascent, scharr, boundary='symm', mode='same')

    >>> import matplotlib.pyplot as plt
    >>> fig, (ax_orig, ax_mag, ax_ang) = plt.subplots(3, 1, figsize=(6, 15))
    >>> ax_orig.imshow(ascent, cmap='gray')
    >>> ax_orig.set_title('Original')
    >>> ax_orig.set_axis_off()
    >>> ax_mag.imshow(np.absolute(grad), cmap='gray')
    >>> ax_mag.set_title('Gradient magnitude')
    >>> ax_mag.set_axis_off()
    >>> ax_ang.imshow(np.angle(grad), cmap='hsv') # hsv is cyclic, like angles
    >>> ax_ang.set_title('Gradient orientation')
    >>> ax_ang.set_axis_off()
    >>> fig.show()

    """
    xp = array_namespace(in1, in2)

    # NB: do work in NumPy, only convert the output

    in1 = np.asarray(in1)
    in2 = np.asarray(in2)

    if not in1.ndim == in2.ndim == 2:
        raise ValueError('convolve2d inputs must both be 2-D arrays')

    if _inputs_swap_needed(mode, in1.shape, in2.shape):
        in1, in2 = in2, in1

    val = _valfrommode(mode)
    bval = _bvalfromboundary(boundary)
    out = _sigtools._convolve2d(in1, in2, 1, val, bval, fillvalue)
    return xp.asarray(out)


def convolve2d(in1: Array, in2: Array, mode: ModeString = 'full', boundary: str = 'fill',
               fillvalue: float = 0, precision: PrecisionLike = None) -> Array:
  """Convolution of two 2-dimensional arrays.

  JAX implementation of :func:`scipy.signal.convolve2d`.

  Args:
    in1: left-hand input to the convolution. Must have ``in1.ndim == 2``.
    in2: right-hand input to the convolution. Must have ``in2.ndim == 2``.
    mode: controls the size of the output. Available operations are:

      * ``"full"``: (default) output the full convolution of the inputs.
      * ``"same"``: return a centered portion of the ``"full"`` output which
        is the same size as ``in1``.
      * ``"valid"``: return the portion of the ``"full"`` output which do not
        depend on padding at the array edges.

    boundary: only ``"fill"`` is supported.
    fillvalue: only ``0`` is supported.
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
    - :func:`jax.scipy.signal.convolve`: ND convolution
    - :func:`jax.scipy.signal.correlate`: ND correlation

  Examples:
    A few 2D convolution examples:

    >>> x = jnp.array([[1, 2],
    ...                [3, 4]])
    >>> y = jnp.array([[2, 1, 1],
    ...                [4, 3, 4],
    ...                [1, 3, 2]])

    Full 2D convolution uses implicit zero-padding at the edges:

    >>> jax.scipy.signal.convolve2d(x, y, mode='full')
    Array([[ 2.,  5.,  3.,  2.],
           [10., 22., 17., 12.],
           [13., 30., 32., 20.],
           [ 3., 13., 18.,  8.]], dtype=float32)

    Specifying ``mode = 'same'`` returns a centered 2D convolution of the same size
    as the first input:

    >>> jax.scipy.signal.convolve2d(x, y, mode='same')
    Array([[22., 17.],
           [30., 32.]], dtype=float32)

    Specifying ``mode = 'valid'`` returns only the portion of 2D convolution
    where the two arrays fully overlap:

    >>> jax.scipy.signal.convolve2d(x, y, mode='valid')
    Array([[22., 17.],
           [30., 32.]], dtype=float32)
  """
  if boundary != 'fill' or fillvalue != 0:
    raise NotImplementedError("convolve2d() only supports boundary='fill', fillvalue=0")
  if np.ndim(in1) != 2 or np.ndim(in2) != 2:
    raise ValueError("convolve2d() only supports 2-dimensional inputs.")
  return _convolve_nd(in1, in2, mode, precision=precision)

