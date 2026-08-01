
def interp(x, xp, fp, left=None, right=None, period=None):
    """
    One-dimensional linear interpolation for monotonically increasing sample points.

    Returns the one-dimensional piecewise linear interpolant to a function
    with given discrete data points (`xp`, `fp`), evaluated at `x`.

    Parameters
    ----------
    x : array_like
        The x-coordinates at which to evaluate the interpolated values.

    xp : 1-D sequence of floats
        The x-coordinates of the data points, must be increasing if argument
        `period` is not specified. Otherwise, `xp` is internally sorted after
        normalizing the periodic boundaries with ``xp = xp % period``.

    fp : 1-D sequence of float or complex
        The y-coordinates of the data points, same length as `xp`.

    left : optional float or complex corresponding to fp
        Value to return for `x < xp[0]`, default is `fp[0]`.

    right : optional float or complex corresponding to fp
        Value to return for `x > xp[-1]`, default is `fp[-1]`.

    period : None or float, optional
        A period for the x-coordinates. This parameter allows the proper
        interpolation of angular x-coordinates. Parameters `left` and `right`
        are ignored if `period` is specified.

    Returns
    -------
    y : float or complex (corresponding to fp) or ndarray
        The interpolated values, same shape as `x`.

    Raises
    ------
    ValueError
        If `xp` and `fp` have different length
        If `xp` or `fp` are not 1-D sequences
        If `period == 0`

    See Also
    --------
    scipy.interpolate

    Warnings
    --------
    The x-coordinate sequence is expected to be increasing, but this is not
    explicitly enforced.  However, if the sequence `xp` is non-increasing,
    interpolation results are meaningless.

    Note that, since NaN is unsortable, `xp` also cannot contain NaNs.

    A simple check for `xp` being strictly increasing is::

        np.all(np.diff(xp) > 0)

    Examples
    --------
    >>> import numpy as np
    >>> xp = [1, 2, 3]
    >>> fp = [3, 2, 0]
    >>> np.interp(2.5, xp, fp)
    1.0
    >>> np.interp([0, 1, 1.5, 2.72, 3.14], xp, fp)
    array([3.  , 3.  , 2.5 , 0.56, 0.  ])
    >>> UNDEF = -99.0
    >>> np.interp(3.14, xp, fp, right=UNDEF)
    -99.0

    Plot an interpolant to the sine function:

    >>> x = np.linspace(0, 2*np.pi, 10)
    >>> y = np.sin(x)
    >>> xvals = np.linspace(0, 2*np.pi, 50)
    >>> yinterp = np.interp(xvals, x, y)
    >>> import matplotlib.pyplot as plt
    >>> plt.plot(x, y, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.plot(xvals, yinterp, '-x')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.show()

    Interpolation with periodic x-coordinates:

    >>> x = [-180, -170, -185, 185, -10, -5, 0, 365]
    >>> xp = [190, -190, 350, -350]
    >>> fp = [5, 10, 3, 4]
    >>> np.interp(x, xp, fp, period=360)
    array([7.5 , 5.  , 8.75, 6.25, 3.  , 3.25, 3.5 , 3.75])

    Complex interpolation:

    >>> x = [1.5, 4.0]
    >>> xp = [2,3,5]
    >>> fp = [1.0j, 0, 2+3j]
    >>> np.interp(x, xp, fp)
    array([0.+1.j , 1.+1.5j])

    """

    fp = np.asarray(fp)

    if np.iscomplexobj(fp):
        interp_func = compiled_interp_complex
        input_dtype = np.complex128
    else:
        interp_func = compiled_interp
        input_dtype = np.float64

    if period is not None:
        if period == 0:
            raise ValueError("period must be a non-zero value")
        period = abs(period)
        left = None
        right = None

        x = np.asarray(x, dtype=np.float64)
        xp = np.asarray(xp, dtype=np.float64)
        fp = np.asarray(fp, dtype=input_dtype)

        if xp.ndim != 1 or fp.ndim != 1:
            raise ValueError("Data points must be 1-D sequences")
        if xp.shape[0] != fp.shape[0]:
            raise ValueError("fp and xp are not of the same length")
        # normalizing periodic boundaries
        x = x % period
        xp = xp % period
        asort_xp = np.argsort(xp)
        xp = xp[asort_xp]
        fp = fp[asort_xp]
        xp = np.concatenate((xp[-1:] - period, xp, xp[0:1] + period))
        fp = np.concatenate((fp[-1:], fp, fp[0:1]))

    return interp_func(x, xp, fp, left, right)


def interp(x: ArrayLike, xp: ArrayLike, fp: ArrayLike,
           left: ArrayLike | str | None = None,
           right: ArrayLike | str | None = None,
           period: ArrayLike | None = None) -> Array:
  """One-dimensional linear interpolation.

  JAX implementation of :func:`numpy.interp`.

  Args:
    x: N-dimensional array of x coordinates at which to evaluate the interpolation.
    xp: one-dimensional sorted array of points to be interpolated.
    fp: array of shape ``xp.shape`` containing the function values associated with ``xp``.
    left: specify how to handle points ``x < xp[0]``. Default is to return ``fp[0]``.
      If ``left`` is a scalar value, it will return this value. if ``left`` is the string
      ``"extrapolate"``, then the value will be determined by linear extrapolation.
      ``left`` is ignored if ``period`` is specified.
    right: specify how to handle points ``x > xp[-1]``. Default is to return ``fp[-1]``.
      If ``right`` is a scalar value, it will return this value. if ``right`` is the string
      ``"extrapolate"``, then the value will be determined by linear extrapolation.
      ``right`` is ignored if ``period`` is specified.
    period: optionally specify the period for the *x* coordinates, for e.g. interpolation
      in angular space.

  Returns:
    an array of shape ``x.shape`` containing the interpolated function at values ``x``.

  Examples:
    >>> xp = jnp.arange(10)
    >>> fp = 2 * xp
    >>> x = jnp.array([0.5, 2.0, 3.5])
    >>> interp(x, xp, fp)
    Array([1., 4., 7.], dtype=float32)

    Unless otherwise specified, extrapolation will be constant:

    >>> x = jnp.array([-10., 10.])
    >>> interp(x, xp, fp)
    Array([ 0., 18.], dtype=float32)

    Use ``"extrapolate"`` mode for linear extrapolation:

    >>> interp(x, xp, fp, left='extrapolate', right='extrapolate')
    Array([-20.,  20.], dtype=float32)

    For periodic interpolation, specify the ``period``:

    >>> xp = jnp.array([0, jnp.pi / 2, jnp.pi, 3 * jnp.pi / 2])
    >>> fp = jnp.sin(xp)
    >>> x = 2 * jnp.pi  # note: not in input array
    >>> jnp.interp(x, xp, fp, period=2 * jnp.pi)
    Array(0., dtype=float32)
  """
  static_argnames = []
  if isinstance(left, str) or left is None:
    static_argnames.append('left')
  if isinstance(right, str) or right is None:
    static_argnames.append('right')
  if period is None:
    static_argnames.append('period')
  jitted_interp = api.jit(_interp, static_argnames=static_argnames)
  return jitted_interp(x, xp, fp, left, right, period)


def interp(
    x: Array['*d'],
    from_: Tuple[_MinMaxValue, _MinMaxValue],
    to: Tuple[_MinMaxValue, _MinMaxValue],
    *,
    axis: int = -1,
    xnp: numpy_utils.NpModule = ...,
) -> FloatArray['*d']:
  """Linearly scale the given value by the given range.

  Somehow similar to `np.interp` or `scipy.interpolate.inter1d` with some
  differences like support scaling an axis by a different factors and
  extrapolate values outside the boundaries.

  `from_` and `to` are expected to be `(min, max)` tuples and the function
  interpolate between the two ranges.

  Example: Normalizing a uint8 image to `(-1, 1)`.

  ```python
  img = jnp.array([
      [0, 0],
      [127, 255],
  ])
  img = enp.interp(img, (0, 255), (0, 1))
  img == jnp.array([
      [-1, -1],
      [0.498..., 1],
  ])
  ```

  `min` and `max` can be either float values or array like structure, in which
  case the numpy broadcasting rules applies (x should be a `Array[... d]` and
  min/max values should be `Array[d]`.

  Example: Converting normalized 3d coordinates to world coordinates.

  ```python
  coords = enp.interp(coords, from_=(-1, 1), to=(0, (h, w, d)))
  ```

  * `coords[:, 0]` is interpolated from `(-1, 1)` to `(0, h)`
  * `coords[:, 1]` is interpolated from `(-1, 1)` to `(0, w)`
  * `coords[:, 2]` is interpolated from `(-1, 1)` to `(0, d)`

  Args:
    x: Array to scale
    from_: Range of x.
    to: Range to which normalize x.
    axis: Axis on which normalizing. Only relevant if `from_` or `to` items
      contains range value.
    xnp: Numpy module to use

  Returns:
    Float tensor with same shape as x, but with normalized coordinates.
  """
  # Could add an `axis` argument.
  # Could add an `fill_values` argument to indicates the behavior if input
  # values are outside the input range. (`error`, `extrapolate` or `truncate`).

  # TODO(epot): Should check if `tnp.experimental_enable_numpy_behavior()`
  # is set, to check whether tf.Tensor need to be explicit casted
  # if lazy.is_tf(x) and x.dtype not in {lazy.tf.float32, lazy.tf.float64}:
  #   raise ValueError(f'`interp` input should be float32. Got: {x.dtype}')

  if axis != -1:
    raise NotImplementedError(
        'Only last axis supported for now. Please send a feature request.'
    )

  # Note: In theory, this could be static arguments so we could use numpy
  # instead of xnp.
  # However torch don't support `torch.Tensor + np.ndarray` and casting
  # `torch.asarray()` afterward seems to create crash
  from_ = tuple(xnp.asarray(v) for v in from_)
  to = tuple(xnp.asarray(v) for v in to)

  # `a` can be scalar or array of shape=(x.shape[-1],), same for `b`
  a, b = _linear_interp_factors(*from_, *to)  # pytype: disable=wrong-arg-types
  return a * x + b

