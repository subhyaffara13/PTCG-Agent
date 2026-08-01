
def geomspace(
    start: ArrayLike,
    stop: ArrayLike,
    num=50,
    endpoint=True,
    dtype: DTypeLike | None = None,
    axis=0,
):
    if axis != 0 or not endpoint:
        raise NotImplementedError
    base = torch.pow(stop / start, 1.0 / (num - 1))
    logbase = torch.log(base)
    return torch.logspace(
        torch.log(start) / logbase,
        torch.log(stop) / logbase,
        num,
        base=base,
    )


def geomspace(start, stop, num=50, endpoint=True, dtype=None, axis=0):
    """
    Return numbers spaced evenly on a log scale (a geometric progression).

    This is similar to `logspace`, but with endpoints specified directly.
    Each output sample is a constant multiple of the previous.

    Parameters
    ----------
    start : array_like
        The starting value of the sequence.
    stop : array_like
        The final value of the sequence, unless `endpoint` is False.
        In that case, ``num + 1`` values are spaced over the
        interval in log-space, of which all but the last (a sequence of
        length `num`) are returned.
    num : integer, optional
        Number of samples to generate.  Default is 50.
    endpoint : boolean, optional
        If true, `stop` is the last sample. Otherwise, it is not included.
        Default is True.
    dtype : dtype
        The type of the output array.  If `dtype` is not given, the data type
        is inferred from `start` and `stop`. The inferred dtype will never be
        an integer; `float` is chosen even if the arguments would produce an
        array of integers.
    axis : int, optional
        The axis in the result to store the samples.  Relevant only if start
        or stop are array-like.  By default (0), the samples will be along a
        new axis inserted at the beginning. Use -1 to get an axis at the end.

    Returns
    -------
    samples : ndarray
        `num` samples, equally spaced on a log scale.

    See Also
    --------
    logspace : Similar to geomspace, but with endpoints specified using log
               and base.
    linspace : Similar to geomspace, but with arithmetic instead of geometric
               progression.
    arange : Similar to linspace, with the step size specified instead of the
             number of samples.
    :ref:`how-to-partition`

    Notes
    -----
    If the inputs or dtype are complex, the output will follow a logarithmic
    spiral in the complex plane.  (There are an infinite number of spirals
    passing through two points; the output will follow the shortest such path.)

    Examples
    --------
    >>> import numpy as np
    >>> np.geomspace(1, 1000, num=4)
    array([    1.,    10.,   100.,  1000.])
    >>> np.geomspace(1, 1000, num=3, endpoint=False)
    array([   1.,   10.,  100.])
    >>> np.geomspace(1, 1000, num=4, endpoint=False)
    array([   1.        ,    5.62341325,   31.6227766 ,  177.827941  ])
    >>> np.geomspace(1, 256, num=9)
    array([   1.,    2.,    4.,    8.,   16.,   32.,   64.,  128.,  256.])

    Note that the above may not produce exact integers:

    >>> np.geomspace(1, 256, num=9, dtype=np.int_)
    array([  1,   2,   4,   7,  16,  32,  63, 127, 256])
    >>> np.around(np.geomspace(1, 256, num=9)).astype(np.int_)
    array([  1,   2,   4,   8,  16,  32,  64, 128, 256])

    Negative, decreasing, and complex inputs are allowed:

    >>> np.geomspace(1000, 1, num=4)
    array([1000.,  100.,   10.,    1.])
    >>> np.geomspace(-1000, -1, num=4)
    array([-1000.,  -100.,   -10.,    -1.])
    >>> np.geomspace(1j, 1000j, num=4)  # Straight line
    array([0.   +1.j, 0.  +10.j, 0. +100.j, 0.+1000.j])
    >>> np.geomspace(-1+0j, 1+0j, num=5)  # Circle
    array([-1.00000000e+00+1.22464680e-16j, -7.07106781e-01+7.07106781e-01j,
            6.12323400e-17+1.00000000e+00j,  7.07106781e-01+7.07106781e-01j,
            1.00000000e+00+0.00000000e+00j])

    Graphical illustration of `endpoint` parameter:

    >>> import matplotlib.pyplot as plt
    >>> N = 10
    >>> y = np.zeros(N)
    >>> plt.semilogx(np.geomspace(1, 1000, N, endpoint=True), y + 1, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.semilogx(np.geomspace(1, 1000, N, endpoint=False), y + 2, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.axis([0.5, 2000, 0, 3])
    [0.5, 2000, 0, 3]
    >>> plt.grid(True, color='0.7', linestyle='-', which='both', axis='both')
    >>> plt.show()

    """
    start = asanyarray(start)
    stop = asanyarray(stop)
    if _nx.any(start == 0) or _nx.any(stop == 0):
        raise ValueError('Geometric sequence cannot include zero')

    dt = result_type(start, stop, float(num), _nx.zeros((), dtype))
    if dtype is None:
        dtype = dt
    else:
        # complex to dtype('complex128'), for instance
        dtype = _nx.dtype(dtype)

    # Promote both arguments to the same dtype in case, for instance, one is
    # complex and another is negative and log would produce NaN otherwise.
    # Copy since we may change things in-place further down.
    start = start.astype(dt, copy=True)
    stop = stop.astype(dt, copy=True)

    # Allow negative real values and ensure a consistent result for complex
    # (including avoiding negligible real or imaginary parts in output) by
    # rotating start to positive real, calculating, then undoing rotation.
    out_sign = _nx.sign(start)
    start /= out_sign
    stop = stop / out_sign

    log_start = _nx.log10(start)
    log_stop = _nx.log10(stop)
    result = logspace(log_start, log_stop, num=num,
                      endpoint=endpoint, base=10.0, dtype=dt)

    # Make sure the endpoints match the start and stop arguments. This is
    # necessary because np.exp(np.log(x)) is not necessarily equal to x.
    if num > 0:
        result[0] = start
        if num > 1 and endpoint:
            result[-1] = stop

    result *= out_sign

    if axis != 0:
        result = _nx.moveaxis(result, 0, axis)

    return result.astype(dtype, copy=False)


def geomspace(start: ArrayLike, stop: ArrayLike, num: int = 50, endpoint: bool = True,
              dtype: DTypeLike | None = None, axis: int = 0) -> Array:
  """Generate geometrically-spaced values.

  JAX implementation of :func:`numpy.geomspace`.

  Args:
    start: scalar or array. Specifies the starting values.
    stop: scalar or array. Specifies the stop values.
    num: int, optional, default=50. Number of values to generate.
    endpoint: bool, optional, default=True. If True, then include the ``stop`` value
      in the result. If False, then exclude the ``stop`` value.
    dtype: optional. Specifies the dtype of the output.
    axis: int, optional, default=0. Axis along which to generate the geomspace.

  Returns:
    An array containing the geometrically-spaced values.

  See also:
    - :func:`jax.numpy.arange`: Generate ``N`` evenly-spaced values given a starting
      point and a step value.
    - :func:`jax.numpy.linspace`: Generate evenly-spaced values.
    - :func:`jax.numpy.logspace`: Generate logarithmically-spaced values.

  Examples:
    List 5 geometrically-spaced values between 1 and 16:

    >>> with jnp.printoptions(precision=3, suppress=True):
    ...   jnp.geomspace(1, 16, 5)
    Array([ 1.,  2.,  4.,  8., 16.], dtype=float32)

    List 4 geomtrically-spaced values between 1 and 16, with ``endpoint=False``:

    >>> with jnp.printoptions(precision=3, suppress=True):
    ...   jnp.geomspace(1, 16, 4, endpoint=False)
    Array([1., 2., 4., 8.], dtype=float32)

    Multi-dimensional geomspace:

    >>> start = jnp.array([1, 1000])
    >>> stop = jnp.array([27, 1])
    >>> with jnp.printoptions(precision=3, suppress=True):
    ...   jnp.geomspace(start, stop, 4)
    Array([[   1., 1000.],
           [   3.,  100.],
           [   9.,   10.],
           [  27.,    1.]], dtype=float32)
  """
  num = core.concrete_or_error(operator.index, num, "'num' argument of jnp.geomspace")
  axis = core.concrete_or_error(operator.index, axis, "'axis' argument of jnp.geomspace")
  return _geomspace(start, stop, num, endpoint, dtype, axis)

