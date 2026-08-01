
def trapezoid(y, x=None, dx=1.0, axis=-1):
    r"""
    Integrate along the given axis using the composite trapezoidal rule.

    If `x` is provided, the integration happens in sequence along its
    elements - they are not sorted.

    Integrate `y` (`x`) along each 1d slice on the given axis, compute
    :math:`\int y(x) dx`.
    When `x` is specified, this integrates along the parametric curve,
    computing :math:`\int_t y(t) dt =
    \int_t y(t) \left.\frac{dx}{dt}\right|_{x=x(t)} dt`.

    Parameters
    ----------
    y : array_like
        Input array to integrate.
    x : array_like, optional
        The sample points corresponding to the `y` values. If `x` is None,
        the sample points are assumed to be evenly spaced `dx` apart. The
        default is None.
    dx : scalar, optional
        The spacing between sample points when `x` is None. The default is 1.
    axis : int, optional
        The axis along which to integrate. The default is the last axis.

    Returns
    -------
    trapezoid : float or ndarray
        Definite integral of `y` = n-dimensional array as approximated along
        a single axis by the trapezoidal rule. If `y` is a 1-dimensional array,
        then the result is a float. If `n` is greater than 1, then the result
        is an `n`-1 dimensional array.

    See Also
    --------
    cumulative_trapezoid, simpson, romb

    Notes
    -----
    Image [2]_ illustrates trapezoidal rule -- y-axis locations of points
    will be taken from `y` array, by default x-axis distances between
    points will be 1.0, alternatively they can be provided with `x` array
    or with `dx` scalar.  Return value will be equal to combined area under
    the red lines.

    References
    ----------
    .. [1] Wikipedia page: https://en.wikipedia.org/wiki/Trapezoidal_rule

    .. [2] Illustration image:
           https://en.wikipedia.org/wiki/File:Composite_trapezoidal_rule_illustration.png

    Examples
    --------
    Use the trapezoidal rule on evenly spaced points:

    >>> import numpy as np
    >>> from scipy import integrate
    >>> integrate.trapezoid([1, 2, 3])
    4.0

    The spacing between sample points can be selected by either the
    ``x`` or ``dx`` arguments:

    >>> integrate.trapezoid([1, 2, 3], x=[4, 6, 8])
    8.0
    >>> integrate.trapezoid([1, 2, 3], dx=2)
    8.0

    Using a decreasing ``x`` corresponds to integrating in reverse:

    >>> integrate.trapezoid([1, 2, 3], x=[8, 6, 4])
    -8.0

    More generally ``x`` is used to integrate along a parametric curve. We can
    estimate the integral :math:`\int_0^1 x^2 = 1/3` using:

    >>> x = np.linspace(0, 1, num=50)
    >>> y = x**2
    >>> integrate.trapezoid(y, x)
    0.33340274885464394

    Or estimate the area of a circle, noting we repeat the sample which closes
    the curve:

    >>> theta = np.linspace(0, 2 * np.pi, num=1000, endpoint=True)
    >>> integrate.trapezoid(np.cos(theta), x=np.sin(theta))
    3.141571941375841

    ``trapezoid`` can be applied along a specified axis to do multiple
    computations in one call:

    >>> a = np.arange(6).reshape(2, 3)
    >>> a
    array([[0, 1, 2],
           [3, 4, 5]])
    >>> integrate.trapezoid(a, axis=0)
    array([1.5, 2.5, 3.5])
    >>> integrate.trapezoid(a, axis=1)
    array([2.,  8.])
    """
    xp = array_namespace(y)
    y = _asarray(y, xp=xp, subok=True)
    # Cannot just use the broadcasted arrays that are returned
    # because trapezoid does not follow normal broadcasting rules
    # cf. https://github.com/scipy/scipy/pull/21524#issuecomment-2354105942
    result_dtype = xp_result_type(y, force_floating=True, xp=xp)
    nd = y.ndim
    slice1 = [slice(None)]*nd
    slice2 = [slice(None)]*nd
    slice1[axis] = slice(1, None)
    slice2[axis] = slice(None, -1)
    if x is None:
        d = dx
    else:
        x = _asarray(x, xp=xp, subok=True)
        if x.ndim == 1:
            d = x[1:] - x[:-1]
            # make d broadcastable to y
            slice3 = [None] * nd
            slice3[axis] = slice(None)
            d = d[tuple(slice3)]
        else:
            # if x is n-D it should be broadcastable to y
            x = xp.broadcast_to(x, y.shape)
            d = x[tuple(slice1)] - x[tuple(slice2)]
    try:
        ret = xp.sum(
            d * (y[tuple(slice1)] + y[tuple(slice2)]) / 2.0,
            axis=axis, dtype=result_dtype
        )
    except ValueError:
        # Operations didn't work, cast to ndarray
        d = xp.asarray(d)
        y = xp.asarray(y)
        ret = xp.sum(
            d * (y[tuple(slice1)] + y[tuple(slice2)]) / 2.0,
            axis=axis, dtype=result_dtype
        )
    return ret


def trapezoid(y, x=None, dx=1.0, axis=-1):
    r"""
    Integrate along the given axis using the composite trapezoidal rule.

    If `x` is provided, the integration happens in sequence along its
    elements - they are not sorted.

    Integrate `y` (`x`) along each 1d slice on the given axis, compute
    :math:`\int y(x) dx`.
    When `x` is specified, this integrates along the parametric curve,
    computing :math:`\int_t y(t) dt =
    \int_t y(t) \left.\frac{dx}{dt}\right|_{x=x(t)} dt`.

    .. versionadded:: 2.0.0

    Parameters
    ----------
    y : array_like
        Input array to integrate.
    x : array_like, optional
        The sample points corresponding to the `y` values. If `x` is None,
        the sample points are assumed to be evenly spaced `dx` apart. The
        default is None.
    dx : scalar, optional
        The spacing between sample points when `x` is None. The default is 1.
    axis : int, optional
        The axis along which to integrate.

    Returns
    -------
    trapezoid : float or ndarray
        Definite integral of `y` = n-dimensional array as approximated along
        a single axis by the trapezoidal rule. If `y` is a 1-dimensional array,
        then the result is a float. If `n` is greater than 1, then the result
        is an `n`-1 dimensional array.

    See Also
    --------
    sum, cumsum

    Notes
    -----
    Image [2]_ illustrates trapezoidal rule -- y-axis locations of points
    will be taken from `y` array, by default x-axis distances between
    points will be 1.0, alternatively they can be provided with `x` array
    or with `dx` scalar.  Return value will be equal to combined area under
    the red lines.


    References
    ----------
    .. [1] Wikipedia page: https://en.wikipedia.org/wiki/Trapezoidal_rule

    .. [2] Illustration image:
           https://en.wikipedia.org/wiki/File:Composite_trapezoidal_rule_illustration.png

    Examples
    --------
    >>> import numpy as np

    Use the trapezoidal rule on evenly spaced points:

    >>> np.trapezoid([1, 2, 3])
    4.0

    The spacing between sample points can be selected by either the
    ``x`` or ``dx`` arguments:

    >>> np.trapezoid([1, 2, 3], x=[4, 6, 8])
    8.0
    >>> np.trapezoid([1, 2, 3], dx=2)
    8.0

    Using a decreasing ``x`` corresponds to integrating in reverse:

    >>> np.trapezoid([1, 2, 3], x=[8, 6, 4])
    -8.0

    More generally ``x`` is used to integrate along a parametric curve. We can
    estimate the integral :math:`\int_0^1 x^2 = 1/3` using:

    >>> x = np.linspace(0, 1, num=50)
    >>> y = x**2
    >>> np.trapezoid(y, x)
    0.33340274885464394

    Or estimate the area of a circle, noting we repeat the sample which closes
    the curve:

    >>> theta = np.linspace(0, 2 * np.pi, num=1000, endpoint=True)
    >>> np.trapezoid(np.cos(theta), x=np.sin(theta))
    3.141571941375841

    ``np.trapezoid`` can be applied along a specified axis to do multiple
    computations in one call:

    >>> a = np.arange(6).reshape(2, 3)
    >>> a
    array([[0, 1, 2],
           [3, 4, 5]])
    >>> np.trapezoid(a, axis=0)
    array([1.5, 2.5, 3.5])
    >>> np.trapezoid(a, axis=1)
    array([2.,  8.])
    """

    y = asanyarray(y)
    if x is None:
        d = dx
    else:
        x = asanyarray(x)
        if x.ndim == 1:
            d = diff(x)
            # reshape to correct shape
            shape = [1] * y.ndim
            shape[axis] = d.shape[0]
            d = d.reshape(shape)
        else:
            d = diff(x, axis=axis)
    nd = y.ndim
    slice1 = [slice(None)] * nd
    slice2 = [slice(None)] * nd
    slice1[axis] = slice(1, None)
    slice2[axis] = slice(None, -1)
    try:
        ret = (d * (y[tuple(slice1)] + y[tuple(slice2)]) / 2.0).sum(axis)
    except ValueError:
        # Operations didn't work, cast to ndarray
        d = np.asarray(d)
        y = np.asarray(y)
        ret = add.reduce(d * (y[tuple(slice1)] + y[tuple(slice2)]) / 2.0, axis)
    return ret


def trapezoid(y: ArrayLike, x: ArrayLike | None = None, dx: ArrayLike = 1.0,
              axis: int = -1) -> Array:
  r"""
  Integrate along the given axis using the composite trapezoidal rule.

  JAX implementation of :func:`numpy.trapezoid`

  The trapezoidal rule approximates the integral under a curve by summing the
  areas of trapezoids formed between adjacent data points.

  Args:
    y: array of data to integrate.
    x: optional array of sample points corresponding to the ``y`` values. If not
       provided, ``x`` defaults to equally spaced with spacing given by ``dx``.
    dx: The spacing between sample points when `x` is None (default: 1.0).
    axis: The axis along which to integrate (default: -1)

  Returns:
    The definite integral approximated by the trapezoidal rule.

  Examples:
    Integrate over a regular grid, with spacing 1.0:

    >>> y = jnp.array([1, 2, 3, 2, 3, 2, 1])
    >>> jnp.trapezoid(y, dx=1.0)
    Array(13., dtype=float32)

    Integrate over an irregular grid:

    >>> x = jnp.array([0, 2, 5, 7, 10, 15, 20])
    >>> jnp.trapezoid(y, x)
    Array(43., dtype=float32)

    Approximate :math:`\int_0^{2\pi} \sin^2(x)dx`, which equals :math:`\pi`:

    >>> x = jnp.linspace(0, 2 * jnp.pi, 1000)
    >>> y = jnp.sin(x) ** 2
    >>> result = jnp.trapezoid(y, x)
    >>> jnp.allclose(result, jnp.pi)
    Array(True, dtype=bool)
  """
  # TODO(phawkins): remove this annotation after fixing jnp types.
  dx_array: Array
  if x is None:
    y = util.ensure_arraylike('trapezoid', y)
    y_arr, = util.promote_dtypes_inexact(y)
    dx_array = asarray(dx)
    if dx_array.ndim > 0:
      dx_array = lax.expand_dims(dx_array, range(y_arr.ndim - dx_array.ndim))
      dx_array = moveaxis(dx_array, axis, -1)
  else:
    y, x = util.ensure_arraylike('trapezoid', y, x)
    y_arr, x_arr = util.promote_dtypes_inexact(y, x)
    if x_arr.ndim == 1:
      dx_array = diff(x_arr)
    else:
      dx_array = moveaxis(diff(x_arr, axis=axis), axis, -1)
  y_arr = moveaxis(y_arr, axis, -1)
  # Fast path: dx is constant along the integration axis.
  if dx_array.ndim == 0 or dx_array.shape[-1] == 1:
    dx_reduced = dx_array if dx_array.ndim == 0 else dx_array[..., 0]
    return dx_reduced * (y_arr.sum(-1) - 0.5 * (y_arr[..., 0] + y_arr[..., -1]))
  return 0.5 * (dx_array * (y_arr[..., 1:] + y_arr[..., :-1])).sum(-1)


def trapezoid(y: ArrayLike, x: ArrayLike | None = None, dx: ArrayLike = 1.0,
              axis: int = -1) -> Array:
  r"""
  Integrate along the given axis using the composite trapezoidal rule.

  JAX implementation of :func:`scipy.integrate.trapezoid`

  The trapezoidal rule approximates the integral under a curve by summing the
  areas of trapezoids formed between adjacent data points.

  Args:
    y: array of data to integrate.
    x: optional array of sample points corresponding to the ``y`` values. If not
       provided, ``x`` defaults to equally spaced with spacing given by ``dx``.
    dx: The spacing between sample points when `x` is None (default: 1.0).
    axis: The axis along which to integrate (default: -1)

  Returns:
    The definite integral approximated by the trapezoidal rule.

  See also:
    :func:`jax.numpy.trapezoid`: NumPy-style API for trapezoidal integration

  Examples:
    Integrate over a regular grid, with spacing 1.0:

    >>> y = jnp.array([1, 2, 3, 2, 3, 2, 1])
    >>> jax.scipy.integrate.trapezoid(y, dx=1.0)
    Array(13., dtype=float32)

    Integrate over an irregular grid:

    >>> x = jnp.array([0, 2, 5, 7, 10, 15, 20])
    >>> jax.scipy.integrate.trapezoid(y, x)
    Array(43., dtype=float32)

    Approximate :math:`\int_0^{2\pi} \sin^2(x)dx`, which equals :math:`\pi`:

    >>> x = jnp.linspace(0, 2 * jnp.pi, 1000)
    >>> y = jnp.sin(x) ** 2
    >>> result = jax.scipy.integrate.trapezoid(y, x)
    >>> jnp.allclose(result, jnp.pi)
    Array(True, dtype=bool)
  """
  return lax_numpy.trapezoid(y, x, dx, axis)

