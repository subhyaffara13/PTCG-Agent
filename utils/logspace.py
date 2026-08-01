
def logspace(
    start,
    stop,
    num=50,
    endpoint=True,
    base=10.0,
    dtype: DTypeLike | None = None,
    axis=0,
):
    if axis != 0 or not endpoint:
        raise NotImplementedError
    return torch.logspace(start, stop, num, base=base, dtype=dtype)


def logspace(
    start: NumberType | TensorLikeType,
    end: NumberType | TensorLikeType,
    steps: NumberType,
    base: NumberType = 10,
    *,
    dtype: torch.dtype | None = None,
    device: DeviceLikeType | None = None,
    layout: torch.layout = torch.strided,
    pin_memory: bool = False,
    requires_grad: bool = False,
) -> TensorLikeType:
    if dtype is None:
        dtype = torch.get_default_dtype()

    # NB: NumPy doesn't have this cast
    if prims.utils.is_integer_dtype(dtype):
        if isinstance(start, FloatLike):
            start = sym_int(start)
        elif isinstance(start, TensorLikeType):
            torch._check(
                start.dim() == 0,
                lambda: "logspace only supports 0-dimensional start and end tensors",
            )
            start = _maybe_convert_to_dtype(start, dtype)
        if isinstance(end, FloatLike):
            end = sym_int(end)
        elif isinstance(end, TensorLikeType):
            torch._check(
                end.dim() == 0,
                lambda: "logspace only supports 0-dimensional start and end tensors",
            )
            end = _maybe_convert_to_dtype(end, dtype)

    if builtins.any(isinstance(arg, complex) for arg in (start, end, steps)):
        default_complex_dtype = utils.corresponding_complex_dtype(
            torch.get_default_dtype()
        )
        dtype = default_complex_dtype
        _dtype = None  # torch.linspace will update the correct dtype
    else:
        _dtype = torch.float64

    if isinstance(base, complex):
        raise AssertionError(f"base must not be complex, got {type(base)}")  # for mypy
    if base < 0:
        raise NotImplementedError
    ret = torch.linspace(  # type: ignore[misc]
        start,  # type: ignore[arg-type]
        end,  # type: ignore[arg-type]
        steps,  # type: ignore[arg-type]
        dtype=_dtype,
        layout=layout,
        device=device,
        pin_memory=pin_memory,
        requires_grad=requires_grad,
    )
    return _maybe_convert_to_dtype(torch.pow(base, ret), dtype)  # type: ignore[arg-type,return-value]


def logspace(start, stop, num=50, endpoint=True, base=10.0, dtype=None,
             axis=0):
    """
    Return numbers spaced evenly on a log scale.

    In linear space, the sequence starts at ``base ** start``
    (`base` to the power of `start`) and ends with ``base ** stop``
    (see `endpoint` below).

    .. versionchanged:: 1.25.0
        Non-scalar 'base` is now supported

    Parameters
    ----------
    start : array_like
        ``base ** start`` is the starting value of the sequence.
    stop : array_like
        ``base ** stop`` is the final value of the sequence, unless `endpoint`
        is False.  In that case, ``num + 1`` values are spaced over the
        interval in log-space, of which all but the last (a sequence of
        length `num`) are returned.
    num : integer, optional
        Number of samples to generate.  Default is 50.
    endpoint : boolean, optional
        If true, `stop` is the last sample. Otherwise, it is not included.
        Default is True.
    base : array_like, optional
        The base of the log space. The step size between the elements in
        ``ln(samples) / ln(base)`` (or ``log_base(samples)``) is uniform.
        Default is 10.0.
    dtype : dtype
        The type of the output array.  If `dtype` is not given, the data type
        is inferred from `start` and `stop`. The inferred type will never be
        an integer; `float` is chosen even if the arguments would produce an
        array of integers.
    axis : int, optional
        The axis in the result to store the samples.  Relevant only if start,
        stop, or base are array-like.  By default (0), the samples will be
        along a new axis inserted at the beginning. Use -1 to get an axis at
        the end.

    Returns
    -------
    samples : ndarray
        `num` samples, equally spaced on a log scale.

    See Also
    --------
    arange : Similar to linspace, with the step size specified instead of the
             number of samples. Note that, when used with a float endpoint, the
             endpoint may or may not be included.
    linspace : Similar to logspace, but with the samples uniformly distributed
               in linear space, instead of log space.
    geomspace : Similar to logspace, but with endpoints specified directly.
    :ref:`how-to-partition`

    Notes
    -----
    If base is a scalar, logspace is equivalent to the code

    >>> y = np.linspace(start, stop, num=num, endpoint=endpoint)
    ... # doctest: +SKIP
    >>> power(base, y).astype(dtype)
    ... # doctest: +SKIP

    Examples
    --------
    >>> import numpy as np
    >>> np.logspace(2.0, 3.0, num=4)
    array([ 100.        ,  215.443469  ,  464.15888336, 1000.        ])
    >>> np.logspace(2.0, 3.0, num=4, endpoint=False)
    array([100.        ,  177.827941  ,  316.22776602,  562.34132519])
    >>> np.logspace(2.0, 3.0, num=4, base=2.0)
    array([4.        ,  5.0396842 ,  6.34960421,  8.        ])
    >>> np.logspace(2.0, 3.0, num=4, base=[2.0, 3.0], axis=-1)
    array([[ 4.        ,  5.0396842 ,  6.34960421,  8.        ],
           [ 9.        , 12.98024613, 18.72075441, 27.        ]])

    Graphical illustration:

    >>> import matplotlib.pyplot as plt
    >>> N = 10
    >>> x1 = np.logspace(0.1, 1, N, endpoint=True)
    >>> x2 = np.logspace(0.1, 1, N, endpoint=False)
    >>> y = np.zeros(N)
    >>> plt.plot(x1, y, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.plot(x2, y + 0.5, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.ylim([-0.5, 1])
    (-0.5, 1)
    >>> plt.show()

    """
    if not isinstance(base, (float, int)) and np.ndim(base):
        # If base is non-scalar, broadcast it with the others, since it
        # may influence how axis is interpreted.
        ndmax = np.broadcast(start, stop, base).ndim
        start, stop, base = (
            np.array(a, copy=None, subok=True, ndmin=ndmax)
            for a in (start, stop, base)
        )
        base = np.expand_dims(base, axis=axis)
    y = linspace(start, stop, num=num, endpoint=endpoint, axis=axis)
    if dtype is None:
        return _nx.power(base, y)
    return _nx.power(base, y).astype(dtype, copy=False)


def logspace(start: ArrayLike, stop: ArrayLike, num: int = 50,
             endpoint: bool = True, base: ArrayLike = 10.0,
             dtype: DTypeLike | None = None, axis: int = 0) -> Array:
  """Generate logarithmically-spaced values.

  JAX implementation of :func:`numpy.logspace`.

  Args:
    start: scalar or array. Used to specify the start value. The start value is
      ``base ** start``.
    stop: scalar or array. Used to specify the stop value. The end value is
      ``base ** stop``.
    num: int, optional, default=50. Number of values to generate.
    endpoint: bool, optional, default=True. If True, then include the ``stop`` value
      in the result. If False, then exclude the ``stop`` value.
    base: scalar or array, optional, default=10. Specifies the base of the logarithm.
    dtype: optional. Specifies the dtype of the output.
    axis: int, optional, default=0. Axis along which to generate the logspace.

  Returns:
    An array of logarithm.

  See also:
    - :func:`jax.numpy.arange`: Generate ``N`` evenly-spaced values given a starting
      point and a step value.
    - :func:`jax.numpy.linspace`: Generate evenly-spaced values.
    - :func:`jax.numpy.geomspace`: Generate geometrically-spaced values.

  Examples:
    List 5 logarithmically spaced values between 1 (``10 ** 0``) and 100
    (``10 ** 2``):

    >>> with jnp.printoptions(precision=3, suppress=True):
    ...   jnp.logspace(0, 2, 5)
    Array([  1.   ,   3.162,  10.   ,  31.623, 100.   ], dtype=float32)

    List 5 logarithmically-spaced values between 1(``10 ** 0``) and 100
    (``10 ** 2``), excluding endpoint:

    >>> with jnp.printoptions(precision=3, suppress=True):
    ...   jnp.logspace(0, 2, 5, endpoint=False)
    Array([ 1.   ,  2.512,  6.31 , 15.849, 39.811], dtype=float32)

    List 7 logarithmically-spaced values between 1 (``2 ** 0``) and 4 (``2 ** 2``)
    with base 2:

    >>> with jnp.printoptions(precision=3, suppress=True):
    ...   jnp.logspace(0, 2, 7, base=2)
    Array([1.   , 1.26 , 1.587, 2.   , 2.52 , 3.175, 4.   ], dtype=float32)

    Multi-dimensional logspace:

    >>> start = jnp.array([0, 5])
    >>> stop = jnp.array([5, 0])
    >>> base = jnp.array([2, 3])
    >>> with jnp.printoptions(precision=3, suppress=True):
    ...   jnp.logspace(start, stop, 5, base=base)
    Array([[  1.   , 243.   ],
           [  2.378,  61.547],
           [  5.657,  15.588],
           [ 13.454,   3.948],
           [ 32.   ,   1.   ]], dtype=float32)
  """
  num = core.concrete_or_error(operator.index, num, "'num' argument of jnp.logspace")
  axis = core.concrete_or_error(operator.index, axis, "'axis' argument of jnp.logspace")
  return _logspace(start, stop, num, endpoint, base, dtype, axis)

