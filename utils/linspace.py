
def linspace(
    start: ArrayLike,
    stop: ArrayLike,
    num=50,
    endpoint=True,
    retstep=False,
    dtype: DTypeLike | None = None,
    axis=0,
):
    if axis != 0 or retstep or not endpoint:
        raise NotImplementedError
    if dtype is None:
        dtype = _dtypes_impl.default_dtypes().float_dtype
    # XXX: raises TypeError if start or stop are not scalars
    return torch.linspace(start, stop, num, dtype=dtype)


def linspace(
    start: NumberType | TensorLikeType,
    end: NumberType | TensorLikeType,
    steps: NumberType,
    *,
    dtype: torch.dtype | None = None,
    device: DeviceLikeType | None = None,
    layout: torch.layout = torch.strided,
    pin_memory: bool = False,
    requires_grad: bool = False,
) -> TensorLikeType:
    if isinstance(start, TensorLikeType):
        torch._check(
            start.dim() == 0,
            lambda: "linspace only supports 0-dimensional start and end tensors",
        )
        start = _maybe_convert_to_dtype(start, highest_precision_float(device))
    if isinstance(end, TensorLikeType):
        torch._check(
            end.dim() == 0,
            lambda: "linspace only supports 0-dimensional start and end tensors",
        )
        end = _maybe_convert_to_dtype(end, highest_precision_float(device))

    if builtins.any(isinstance(arg, complex) for arg in (start, end, steps)):
        default_complex_dtype = utils.corresponding_complex_dtype(
            torch.get_default_dtype()
        )
        if dtype is None:
            dtype = default_complex_dtype
        else:
            torch._check(
                utils.is_complex_dtype(dtype),
                lambda: f"linspace(): inferred dtype {default_complex_dtype} can't be safely cast to passed dtype {dtype}",
            )
    else:
        dtype = dtype or torch.get_default_dtype()
    if not isinstance(dtype, torch.dtype):
        raise AssertionError(f"dtype must be torch.dtype, got {type(dtype)}")

    # steps does not participate in the computation of the dtype
    torch._check_type(
        isinstance(steps, IntLike),
        lambda: f"received an invalid combination of arguments - got \
({type(start).__name__}, {type(end).__name__}, {type(steps).__name__})",
    )
    if not isinstance(steps, IntLike):
        raise AssertionError(f"steps must be IntLike, got {type(steps)}")  # for mypy
    torch._check(steps >= 0, lambda: "number of steps must be non-negative")

    factory_kwargs = {
        "layout": layout,
        "device": device,
        "pin_memory": pin_memory,
        "requires_grad": requires_grad,
    }
    if steps == 0:
        return torch.full((0,), 0, dtype=dtype, **factory_kwargs)  # type: ignore[arg-type]
    if steps == 1:
        if isinstance(start, TensorLikeType):
            empty_tensor = torch.empty((steps,), dtype=dtype, **factory_kwargs)  # type: ignore[arg-type]
            return torch.ops.aten.copy.default(empty_tensor, start)
        else:
            return torch.full((steps,), start, dtype=dtype, **factory_kwargs)  # type: ignore[arg-type]

    # Perform in arange in int because some backends like ATen or Triton do not support all the dtypes
    rg = torch.arange(0, steps, **factory_kwargs)  # type: ignore[arg-type]

    # Small types need to be computed in higher precision as this is, at heart, an associative scan
    dtype_red = (
        torch.int64
        if (utils.is_boolean_dtype(dtype) or utils.is_integer_dtype(dtype))
        else dtype
    )
    computation_dtype, _ = utils.reduction_dtypes(
        rg, REDUCTION_OUTPUT_TYPE_KIND.SAME, dtype_red
    )
    cast_rg = partial(_maybe_convert_to_dtype, dtype=computation_dtype)

    # We implement torch.lerp without performing rg / (steps - 1) explicitly
    # With this we get out[0] == start, out[-1] == end
    step = (end - start) / (steps - 1)
    # pyrefly: ignore [no-matching-overload]
    out = torch.where(
        rg < steps / 2,
        start + step * cast_rg(rg),  # type: ignore[arg-type,operator]
        end - step * cast_rg((steps - 1) - rg),  # type: ignore[arg-type,operator]
    )
    return _maybe_convert_to_dtype(out, dtype)  # type: ignore[return-value]


def linspace(
    g: jit_utils.GraphContext, start, end, steps, dtype, layout, device, pin_memory
):
    range_tensor = symbolic_helper._arange_helper(g, steps, None)
    step = div(
        g,
        sub(g, end, start),
        sub(g, steps, g.op("Constant", value_t=torch.tensor(1, dtype=torch.int64))),
    )
    return add(g, mul(g, range_tensor, step), start)


def linspace(start, stop, num):
    return [start + (stop - start) * x / (num-1) for x in range(num)]


def linspace(
    start: float,
    stop: float,
    /,
    num: int,
    *,
    xp: Namespace,
    dtype: DType | None = None,
    device: Device | None = None,
    endpoint: bool = True,
    **kwargs: object,
) -> Array:
    _check_device(xp, device)
    return xp.linspace(start, stop, num, dtype=dtype, endpoint=endpoint, **kwargs)


def linspace(start: float,
             stop: float,
             /,
             num: int,
             *,
             dtype: DType | None = None,
             device: Device | None = None,
             endpoint: bool = True,
             **kwargs: object) -> Array:
    if not endpoint:
        return torch.linspace(start, stop, num+1, dtype=dtype, device=device, **kwargs)[:-1]
    return torch.linspace(start, stop, num, dtype=dtype, device=device, **kwargs)


def linspace(start, stop, num=50, endpoint=True, retstep=False, dtype=None,
             axis=0, *, device=None):
    """
    Return evenly spaced numbers over a specified interval.

    Returns `num` evenly spaced samples, calculated over the
    interval [`start`, `stop`].

    The endpoint of the interval can optionally be excluded.

    .. versionchanged:: 1.20.0
        Values are rounded towards ``-inf`` instead of ``0`` when an
        integer ``dtype`` is specified. The old behavior can
        still be obtained with ``np.linspace(start, stop, num).astype(np.int_)``

    Parameters
    ----------
    start : array_like
        The starting value of the sequence.
    stop : array_like
        The end value of the sequence, unless `endpoint` is set to False.
        In that case, the sequence consists of all but the last of ``num + 1``
        evenly spaced samples, so that `stop` is excluded.  Note that the step
        size changes when `endpoint` is False.
    num : int, optional
        Number of samples to generate. Default is 50. Must be non-negative.
    endpoint : bool, optional
        If True, `stop` is the last sample. Otherwise, it is not included.
        Default is True.
    retstep : bool, optional
        If True, return (`samples`, `step`), where `step` is the spacing
        between samples.
    dtype : dtype, optional
        The type of the output array.  If `dtype` is not given, the data type
        is inferred from `start` and `stop`. The inferred dtype will never be
        an integer; `float` is chosen even if the arguments would produce an
        array of integers.
    axis : int, optional
        The axis in the result to store the samples.  Relevant only if start
        or stop are array-like.  By default (0), the samples will be along a
        new axis inserted at the beginning. Use -1 to get an axis at the end.
    device : str, optional
        The device on which to place the created array. Default: None.
        For Array-API interoperability only, so must be ``"cpu"`` if passed.

        .. versionadded:: 2.0.0

    Returns
    -------
    samples : ndarray
        There are `num` equally spaced samples in the closed interval
        ``[start, stop]`` or the half-open interval ``[start, stop)``
        (depending on whether `endpoint` is True or False).
    step : float, optional
        Only returned if `retstep` is True

        Size of spacing between samples.


    See Also
    --------
    arange : Similar to `linspace`, but uses a step size (instead of the
             number of samples).
    geomspace : Similar to `linspace`, but with numbers spaced evenly on a log
                scale (a geometric progression).
    logspace : Similar to `geomspace`, but with the end points specified as
               logarithms.
    :ref:`how-to-partition`

    Examples
    --------
    >>> import numpy as np
    >>> np.linspace(2.0, 3.0, num=5)
    array([2.  , 2.25, 2.5 , 2.75, 3.  ])
    >>> np.linspace(2.0, 3.0, num=5, endpoint=False)
    array([2. ,  2.2,  2.4,  2.6,  2.8])
    >>> np.linspace(2.0, 3.0, num=5, retstep=True)
    (array([2.  ,  2.25,  2.5 ,  2.75,  3.  ]), 0.25)

    Graphical illustration:

    >>> import matplotlib.pyplot as plt
    >>> N = 8
    >>> y = np.zeros(N)
    >>> x1 = np.linspace(0, 10, N, endpoint=True)
    >>> x2 = np.linspace(0, 10, N, endpoint=False)
    >>> plt.plot(x1, y, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.plot(x2, y + 0.5, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.ylim([-0.5, 1])
    (-0.5, 1)
    >>> plt.show()

    """
    num = operator.index(num)
    if num < 0:
        raise ValueError(
            f"Number of samples, {num}, must be non-negative."
        )
    div = (num - 1) if endpoint else num

    conv = _array_converter(start, stop)
    start, stop = conv.as_arrays()
    dt = conv.result_type(ensure_inexact=True)

    if dtype is None:
        dtype = dt
        integer_dtype = False
    else:
        integer_dtype = _nx.issubdtype(dtype, _nx.integer)

    # Use `dtype=type(dt)` to enforce a floating point evaluation:
    delta = np.subtract(stop, start, dtype=type(dt))
    y = _nx.arange(
        0, num, dtype=dt, device=device
    ).reshape((-1,) + (1,) * ndim(delta))

    # In-place multiplication y *= delta/div is faster, but prevents
    # the multiplicant from overriding what class is produced, and thus
    # prevents, e.g. use of Quantities, see gh-7142. Hence, we multiply
    # in place only for standard scalar types.
    if div > 0:
        _mult_inplace = _nx.isscalar(delta)
        step = delta / div
        any_step_zero = (
            step == 0 if _mult_inplace else _nx.asanyarray(step == 0).any())
        if any_step_zero:
            # Special handling for denormal numbers, gh-5437
            y /= div
            if _mult_inplace:
                y *= delta
            else:
                y = y * delta
        elif _mult_inplace:
            y *= step
        else:
            y = y * step
    else:
        # sequences with 0 items or 1 item with endpoint=True (i.e. div <= 0)
        # have an undefined step
        step = nan
        # Multiply with delta to allow possible override of output class.
        y = y * delta

    y += start

    if endpoint and num > 1:
        y[-1, ...] = stop

    if axis != 0:
        y = _nx.moveaxis(y, 0, axis)

    if integer_dtype:
        _nx.floor(y, out=y)

    y = conv.wrap(y.astype(dtype, copy=False))
    if retstep:
        return y, step
    else:
        return y


def linspace(start: ArrayLike, stop: ArrayLike, num: int = 50,
             endpoint: bool = True, retstep: Literal[False] = False,
             dtype: DTypeLike | None = None,
             axis: int = 0,
             *, device: xc.Device | Sharding | None = None) -> Array: ...


def linspace(start: ArrayLike, stop: ArrayLike, num: int,
             endpoint: bool, retstep: Literal[True],
             dtype: DTypeLike | None = None,
             axis: int = 0,
             *, device: xc.Device | Sharding | None = None) -> tuple[Array, Array]: ...


def linspace(start: ArrayLike, stop: ArrayLike, num: int = 50,
             endpoint: bool = True, *, retstep: Literal[True],
             dtype: DTypeLike | None = None,
             axis: int = 0,
             device: xc.Device | Sharding | None = None) -> tuple[Array, Array]: ...


def linspace(start: ArrayLike, stop: ArrayLike, num: int = 50,
             endpoint: bool = True, retstep: bool = False,
             dtype: DTypeLike | None = None,
             axis: int = 0,
             *, device: xc.Device | Sharding | None = None) -> Array | tuple[Array, Array]: ...


def linspace(start: ArrayLike, stop: ArrayLike, num: int = 50,
             endpoint: bool = True, retstep: bool = False,
             dtype: DTypeLike | None = None,
             axis: int = 0,
             *, device: xc.Device | Sharding | None = None) -> Array | tuple[Array, Array]:
  """Return evenly-spaced numbers within an interval.

  JAX implementation of :func:`numpy.linspace`.

  Args:
    start: scalar or array of starting values.
    stop: scalar or array of stop values.
    num: number of values to generate. Default: 50.
    endpoint: if True (default) then include the ``stop`` value in the result.
      If False, then exclude the ``stop`` value.
    retstep: If True, then return a ``(result, step)`` tuple, where ``step`` is the
      interval between adjacent values in ``result``.
    axis: integer axis along which to generate the linspace. Defaults to zero.
    device: optional :class:`~jax.Device` or :class:`~jax.sharding.Sharding`
      to which the created array will be committed.

  Returns:
    An array ``values``, or a tuple ``(values, step)`` if ``retstep`` is True, where:

    - ``values`` is an array of evenly-spaced values from ``start`` to ``stop``
    - ``step`` is the interval between adjacent values.

  See also:
    - :func:`jax.numpy.arange`: Generate ``N`` evenly-spaced values given a starting
      point and a step
    - :func:`jax.numpy.logspace`: Generate logarithmically-spaced values.
    - :func:`jax.numpy.geomspace`: Generate geometrically-spaced values.

  Examples:
    List of 5 values between 0 and 10:

    >>> jnp.linspace(0, 10, 5)
    Array([ 0. ,  2.5,  5. ,  7.5, 10. ], dtype=float32)

    List of 8 values between 0 and 10, excluding the endpoint:

    >>> jnp.linspace(0, 10, 8, endpoint=False)
    Array([0.  , 1.25, 2.5 , 3.75, 5.  , 6.25, 7.5 , 8.75], dtype=float32)

    List of values and the step size between them

    >>> vals, step = jnp.linspace(0, 10, 9, retstep=True)
    >>> vals
    Array([ 0.  ,  1.25,  2.5 ,  3.75,  5.  ,  6.25,  7.5 ,  8.75, 10.  ],      dtype=float32)
    >>> step
    Array(1.25, dtype=float32)

    Multi-dimensional linspace:

    >>> start = jnp.array([0, 5])
    >>> stop = jnp.array([5, 10])
    >>> jnp.linspace(start, stop, 5)
    Array([[ 0.  ,  5.  ],
           [ 1.25,  6.25],
           [ 2.5 ,  7.5 ],
           [ 3.75,  8.75],
           [ 5.  , 10.  ]], dtype=float32)
  """
  num = core.concrete_dim_or_error(num, "'num' argument of jnp.linspace")
  axis = core.concrete_or_error(operator.index, axis, "'axis' argument of jnp.linspace")
  return _linspace(start, stop, num, endpoint, retstep, dtype, axis, device=device)

