
def map_coordinates(input, coordinates, output=None, order=3,
                    mode='constant', cval=0.0, prefilter=True):
    """
    Map the input array to new coordinates by interpolation.

    The array of coordinates is used to find, for each point in the output,
    the corresponding coordinates in the input. The value of the input at
    those coordinates is determined by spline interpolation of the
    requested order.

    The shape of the output is derived from that of the coordinate
    array by dropping the first axis. The values of the array along
    the first axis are the coordinates in the input array at which the
    output value is found.

    Parameters
    ----------
    %(input)s
    coordinates : array_like
        The coordinates at which `input` is evaluated.
    %(output)s
    order : int, optional
        The order of the spline interpolation, default is 3.
        The order has to be in the range 0-5.
    %(mode_interp_constant)s
    %(cval)s
    %(prefilter)s

    Returns
    -------
    map_coordinates : ndarray
        The result of transforming the input. The shape of the output is
        derived from that of `coordinates` by dropping the first axis.

    See Also
    --------
    spline_filter, geometric_transform, scipy.interpolate

    Notes
    -----
    For complex-valued `input`, this function maps the real and imaginary
    components independently.

    .. versionadded:: 1.6.0
        Complex-valued support added.

    Examples
    --------
    >>> from scipy import ndimage
    >>> import numpy as np
    >>> a = np.arange(12.).reshape((4, 3))
    >>> a
    array([[  0.,   1.,   2.],
           [  3.,   4.,   5.],
           [  6.,   7.,   8.],
           [  9.,  10.,  11.]])
    >>> ndimage.map_coordinates(a, [[0.5, 2], [0.5, 1]], order=1)
    array([ 2.,  7.])

    Above, the interpolated value of a[0.5, 0.5] gives output[0], while
    a[2, 1] is output[1].

    >>> inds = np.array([[0.5, 2], [0.5, 4]])
    >>> ndimage.map_coordinates(a, inds, order=1, cval=-33.3)
    array([  2. , -33.3])
    >>> ndimage.map_coordinates(a, inds, order=1, mode='nearest')
    array([ 2.,  8.])
    >>> ndimage.map_coordinates(a, inds, order=1, cval=0, output=bool)
    array([ True, False], dtype=bool)

    """
    if order < 0 or order > 5:
        raise RuntimeError('spline order not supported')
    input = np.asarray(input)
    coordinates = np.asarray(coordinates)
    if np.iscomplexobj(coordinates):
        raise TypeError('Complex type not supported')
    output_shape = coordinates.shape[1:]
    if input.ndim < 1 or len(output_shape) < 1:
        raise RuntimeError('input and output rank must be > 0')
    if coordinates.shape[0] != input.ndim:
        raise RuntimeError('invalid shape for coordinate array')
    complex_output = np.iscomplexobj(input)
    output = _ni_support._get_output(output, input, shape=output_shape,
                                     complex_output=complex_output)
    if complex_output:
        kwargs = dict(order=order, mode=mode, prefilter=prefilter)
        map_coordinates(input.real, coordinates, output=output.real,
                        cval=np.real(cval), **kwargs)
        map_coordinates(input.imag, coordinates, output=output.imag,
                        cval=np.imag(cval), **kwargs)
        return output
    if prefilter and order > 1:
        padded, npad = _prepad_for_spline_filter(input, mode, cval)
        filtered = spline_filter(padded, order, output=np.float64, mode=mode)
    else:
        npad = 0
        filtered = input
    mode = _ni_support._extend_mode_to_code(mode)
    _nd_image.geometric_transform(filtered, None, coordinates, None, None,
                                  output, order, mode, cval, npad, None, None)
    return output


def map_coordinates(
    input: ArrayLike, coordinates: Sequence[ArrayLike], order: int,
    mode: str = 'constant', cval: ArrayLike = 0.0,
):
  """
  Map the input array to new coordinates using interpolation.

  JAX implementation of :func:`scipy.ndimage.map_coordinates`

  Given an input array and a set of coordinates, this function returns the
  interpolated values of the input array at those coordinates.

  Args:
    input: N-dimensional input array from which values are interpolated.
    coordinates: length-N sequence of arrays specifying the coordinates
      at which to evaluate the interpolated values
    order: The order of interpolation. JAX supports the following:

      * 0: Nearest-neighbor
      * 1: Linear

    mode: Points outside the boundaries of the input are filled according to the given mode.
      JAX supports one of ``('constant', 'nearest', 'mirror', 'wrap', 'reflect')``. Note the
      ``'wrap'`` mode in JAX behaves as ``'grid-wrap'`` mode in SciPy, and ``'constant'``
      mode in JAX behaves as ``'grid-constant'`` mode in SciPy. This discrepancy was caused
      by a former bug in those modes in SciPy (https://github.com/scipy/scipy/issues/2640),
      which was first fixed in JAX by changing the behavior of the existing modes, and later
      on fixed in SciPy, by adding modes with new names, rather than fixing the existing
      ones, for backwards compatibility reasons. Default is 'constant'.
    cval: Value used for points outside the boundaries of the input if ``mode='constant'``
      Default is 0.0.

  Returns:
    The interpolated values at the specified coordinates.

  Examples:
    >>> input = jnp.arange(12.0).reshape(3, 4)
    >>> input
    Array([[ 0.,  1.,  2.,  3.],
           [ 4.,  5.,  6.,  7.],
           [ 8.,  9., 10., 11.]], dtype=float32)
    >>> coordinates = [jnp.array([0.5, 1.5]),
    ...                jnp.array([1.5, 2.5])]
    >>> jax.scipy.ndimage.map_coordinates(input, coordinates, order=1)
    Array([3.5, 8.5], dtype=float32)

  Note:
    Interpolation near boundaries differs from the scipy function, because JAX
    fixed an outstanding bug; see https://github.com/jax-ml/jax/issues/11097.
    This function interprets the ``mode`` argument as documented by SciPy, but
    not as implemented by SciPy.
  """
  return _map_coordinates(input, coordinates, order, mode, cval)

