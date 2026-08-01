
def correlate2d(in1, in2, mode='full', boundary='fill', fillvalue=0):
    """
    Cross-correlate two 2-dimensional arrays.

    Cross correlate `in1` and `in2` with output size determined by `mode`, and
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
           The output is the full discrete linear cross-correlation
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
    correlate2d : ndarray
        A 2-dimensional array containing a subset of the discrete linear
        cross-correlation of `in1` with `in2`.

    Notes
    -----
    When using "same" mode with even-length inputs, the outputs of `correlate`
    and `correlate2d` differ: There is a 1-index offset between them.

    Examples
    --------
    Use 2D cross-correlation to find the location of a template in a noisy
    image:

    >>> import numpy as np
    >>> from scipy import signal, datasets, ndimage
    >>> rng = np.random.default_rng()
    >>> face = datasets.face(gray=True) - datasets.face(gray=True).mean()
    >>> face = ndimage.zoom(face[30:500, 400:950], 0.5)  # extract the face
    >>> template = np.copy(face[135:165, 140:175])  # right eye
    >>> template -= template.mean()
    >>> face = face + rng.standard_normal(face.shape) * 50  # add noise
    >>> corr = signal.correlate2d(face, template, boundary='symm', mode='same')
    >>> y, x = np.unravel_index(np.argmax(corr), corr.shape)  # find the match

    >>> import matplotlib.pyplot as plt
    >>> fig, (ax_orig, ax_template, ax_corr) = plt.subplots(3, 1,
    ...                                                     figsize=(6, 15))
    >>> ax_orig.imshow(face, cmap='gray')
    >>> ax_orig.set_title('Original')
    >>> ax_orig.set_axis_off()
    >>> ax_template.imshow(template, cmap='gray')
    >>> ax_template.set_title('Template')
    >>> ax_template.set_axis_off()
    >>> ax_corr.imshow(corr, cmap='gray')
    >>> ax_corr.set_title('Cross-correlation')
    >>> ax_corr.set_axis_off()
    >>> ax_orig.plot(x, y, 'ro')
    >>> fig.show()

    """
    xp = array_namespace(in1, in2)
    in1 = np.asarray(in1)
    in2 = np.asarray(in2)

    if not in1.ndim == in2.ndim == 2:
        raise ValueError('correlate2d inputs must both be 2-D arrays')

    swapped_inputs = _inputs_swap_needed(mode, in1.shape, in2.shape)
    if swapped_inputs:
        in1, in2 = in2, in1

    val = _valfrommode(mode)
    bval = _bvalfromboundary(boundary)
    out = _sigtools._convolve2d(in1, in2.conj(), 0, val, bval, fillvalue)

    if swapped_inputs:
        out = out[::-1, ::-1]

    return xp.asarray(out)


def correlate2d(in1: Array, in2: Array, mode: ModeString = 'full', boundary: str = 'fill',
                fillvalue: float = 0, precision: PrecisionLike = None) -> Array:
  """Cross-correlation of two 2-dimensional arrays.

  JAX implementation of :func:`scipy.signal.correlate2d`.

  Args:
    in1: left-hand input to the cross-correlation. Must have ``in1.ndim == 2``.
    in2: right-hand input to the cross-correlation. Must have ``in2.ndim == 2``.
    mode: controls the size of the output. Available operations are:

      * ``"full"``: (default) output the full cross-correlation of the inputs.
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
    Array containing the cross-correlation result.

  See Also:
    - :func:`jax.numpy.correlate`: 1D cross-correlation
    - :func:`jax.scipy.signal.correlate`: ND cross-correlation
    - :func:`jax.scipy.signal.convolve`: ND convolution

  Examples:
    A few 2D correlation examples:

    >>> x = jnp.array([[2, 1, 3],
    ...                [1, 3, 1],
    ...                [4, 1, 2]])
    >>> y = jnp.array([[1, 3],
    ...                [4, 2]])

    Full 2D correlation uses implicit zero-padding at the edges:

    >>> jax.scipy.signal.correlate2d(x, y, mode='full')
    Array([[ 4., 10., 10., 12.],
           [ 8., 15., 24.,  7.],
           [11., 28., 14.,  9.],
           [12.,  7.,  7.,  2.]], dtype=float32)

    Specifying ``mode = 'same'`` returns a centered 2D correlation of the same
    size as the first input:

    >>> jax.scipy.signal.correlate2d(x, y, mode='same')
    Array([[15., 24.,  7.],
           [28., 14.,  9.],
           [ 7.,  7.,  2.]], dtype=float32)

    Specifying ``mode = 'valid'`` returns only the portion of 2D correlation
    where the two arrays fully overlap:

    >>> jax.scipy.signal.correlate2d(x, y, mode='valid')
    Array([[15., 24.],
           [28., 14.]], dtype=float32)
  """
  if boundary != 'fill' or fillvalue != 0:
    raise NotImplementedError("correlate2d() only supports boundary='fill', fillvalue=0")
  if np.ndim(in1) != 2 or np.ndim(in2) != 2:
    raise ValueError("correlate2d() only supports 2-dimensional inputs.")

  swap = all(s1 <= s2 for s1, s2 in zip(in1.shape, in2.shape))
  same_shape =  all(s1 == s2 for s1, s2 in zip(in1.shape, in2.shape))

  if mode == "same":
    in1, in2 = jnp.flip(in1), in2.conj()
    result = jnp.flip(_convolve_nd(in1, in2, mode, precision=precision))
  elif mode == "valid":
    if swap and not same_shape:
      in1, in2 = jnp.flip(in2), in1.conj()
      result = _convolve_nd(in1, in2, mode, precision=precision)
    else:
      in1, in2 = jnp.flip(in1), in2.conj()
      result = jnp.flip(_convolve_nd(in1, in2, mode, precision=precision))
  else:
    if swap:
      in1, in2 = jnp.flip(in2), in1.conj()
      result = _convolve_nd(in1, in2, mode, precision=precision).conj()
    else:
      in1, in2 = jnp.flip(in1), in2.conj()
      result = jnp.flip(_convolve_nd(in1, in2, mode, precision=precision))
  return result

