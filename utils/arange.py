
def arange(
    start: ArrayLikeOrScalar | None = None,
    stop: ArrayLikeOrScalar | None = None,
    step: ArrayLikeOrScalar | None = 1,
    dtype: DTypeLike | None = None,
    *,
    like: NotImplementedType = None,
):
    if step == 0:
        raise ZeroDivisionError
    if stop is None and start is None:
        raise TypeError
    if stop is None:
        # XXX: this breaks if start is passed as a kwarg:
        # arange(start=4) should raise (no stop) but doesn't
        start, stop = 0, start
    if start is None:
        start = 0

    # the dtype of the result
    if dtype is None:
        dtype = (
            _dtypes_impl.default_dtypes().float_dtype
            if any(_dtypes_impl.is_float_or_fp_tensor(x) for x in (start, stop, step))
            else _dtypes_impl.default_dtypes().int_dtype
        )
    work_dtype = torch.float64 if dtype.is_complex else dtype

    # RuntimeError: "lt_cpu" not implemented for 'ComplexFloat'. Fall back to eager.
    if any(_dtypes_impl.is_complex_or_complex_tensor(x) for x in (start, stop, step)):
        raise NotImplementedError

    if (step > 0 and start > stop) or (step < 0 and start < stop):
        # empty range
        return torch.empty(0, dtype=dtype)

    result = torch.arange(start, stop, step, dtype=work_dtype)
    result = _util.cast_if_needed(result, dtype)
    return result


def arange(
    start: NumberType = 0,
    end: NumberType | None = None,
    step: NumberType = 1,
    *,
    dtype: torch.dtype | None = None,
    layout: torch.layout = torch.strided,
    device: DeviceLikeType | None = None,
    pin_memory: bool = False,
    requires_grad: bool = False,
) -> TensorLikeType:
    utils.check_layout(layout)
    utils.check_pin_memory(pin_memory)
    device = torch.device(utils.device_or_default(device))

    if isinstance(start, complex):
        raise AssertionError("arange does not support complex start")
    if isinstance(end, complex):
        raise AssertionError("arange does not support complex end")
    if isinstance(step, complex):
        raise AssertionError("arange does not support complex step")

    # Case: torch.arange(5)
    if end is None:
        end = start
        start = 0
    torch._check(step != 0, lambda: "step must be nonzero")
    if step > 0:
        torch._check(
            end >= start,
            lambda: "upper bound and lower bound inconsistent with step sign",
        )
    elif step < 0:
        torch._check(
            end <= start,
            lambda: "upper bound and lower bound inconsistent with step sign",
        )

    def is_finite(x):
        return not isinstance(x, FloatWithoutSymFloat) or math.isfinite(x)

    torch._check(
        is_finite(start) and is_finite(end),
        lambda: f"unsupported range: {start} -> {end}",
    )
    torch._check(
        is_finite(step),
        lambda: f"step must be finite but got {step}",
    )

    args = (start, end, step)
    integer_args = builtins.all(isinstance(arg, IntLike) for arg in args)

    if dtype is None:
        dtype = torch.int64 if integer_args else torch.get_default_dtype()

    is_integer = utils.is_integer_dtype(dtype)
    if is_integer or integer_args:
        xstart = sym_int(start)
        xend = sym_int(end)
        xstep = sym_int(step)

    # For int64 we truncate arguments to int before calculating length, but
    # other integral dtypes we don't. Weird... but needed to match ATen shapes.
    if dtype == torch.int64 or integer_args:
        # Uses floordiv to avoid ceil in inductor.
        sgn = bool(xstep > 0) - bool(xstep < 0)  # type: ignore[possibly-undefined]
        length = (xend - xstart + xstep - sgn) // xstep  # type: ignore[possibly-undefined]
    else:
        length = math.ceil((end - start) / step)

    if is_integer:
        return prims.iota(
            length,
            start=xstart,  # type: ignore[possibly-undefined]
            step=xstep,  # type: ignore[possibly-undefined]
            dtype=dtype,
            device=device,
            requires_grad=requires_grad,
        )

    index = prims.iota(
        length,
        start=0,
        step=1,
        dtype=torch.int64,
        device=device,
        requires_grad=False,
    )

    computation_dtype = (
        torch.long if integer_args else utils.get_acc_type(dtype, device)
    )
    index = _maybe_convert_to_dtype(index, computation_dtype)
    result = start + step * index
    result = _maybe_convert_to_dtype(result, dtype)

    if requires_grad:
        result.requires_grad_(True)
    return result


def arange(g: jit_utils.GraphContext, *args):
    def _get_arange_dtype(dtype):
        dtype = symbolic_helper._maybe_get_const(dtype, "i")
        return dtype

    if len(args) == 2 and all(isinstance(val, int) for val in args):
        # aten::arange(Scalar start, Scalar end)
        dtype = torch.int64
        # Start index.
        start = g.op(
            "Constant",
            value_t=torch.tensor(args[0], dtype=dtype),
        )
        # End (exclusive) index.
        end = g.op(
            "Constant",
            value_t=torch.tensor(args[1], dtype=dtype),
        )
        # Step size from start to end indexes.
        delta_default = g.op(
            "Constant",
            value_t=torch.tensor(1, dtype=dtype),
        )
        return g.op("Range", start, end, delta_default)
    elif len(args) == 2 or len(args) == 5:
        if len(args) == 2:
            # aten::arange(Scalar end, Tensor out)
            dtype = None
        else:
            # aten::arange(Scalar end, ScalarType dtype, Layout, Device, bool pin_memory)
            dtype = _get_arange_dtype(args[1])
        type_, end, start, step = symbolic_helper._arange_cast_helper(
            g, end=args[0], dtype=dtype
        )
        start_default = g.op(
            "Constant",
            value_t=torch.tensor(0, dtype=type_.dtype()),
        )
        delta_default = g.op(
            "Constant",
            value_t=torch.tensor(1, dtype=type_.dtype()),
        )
        # pyrefly: ignore [bad-argument-type]
        return g.op("Range", start_default, end, delta_default)
    elif len(args) == 4 or len(args) == 7:
        if len(args) == 4:
            # aten::arange(Scalar start, Scalar end, Scalar step, Tensor out)
            dtype = None
        else:
            # aten::arange(Scalar start, Scalar end, Scalar step, ScalarType dtype, Layout, Device, bool pin_memory)
            dtype = _get_arange_dtype(args[3])
        _, end, start, step = symbolic_helper._arange_cast_helper(
            g, start=args[0], end=args[1], step=args[2], dtype=dtype
        )
        # pyrefly: ignore [bad-argument-type]
        return g.op("Range", start, end, step)
    elif len(args) == 6:
        # aten::arange(Scalar start, Scalar end, ScalarType dtype, Layout, Device, bool pin_memory)
        dtype = _get_arange_dtype(args[2])
        type_, end, start, step = symbolic_helper._arange_cast_helper(
            g, start=args[0], end=args[1], dtype=dtype
        )
        delta_default = g.op(
            "Constant",
            value_t=torch.tensor(1, dtype=type_.dtype()),
        )
        # pyrefly: ignore [bad-argument-type]
        return g.op("Range", start, end, delta_default)
    else:
        return symbolic_helper._unimplemented(
            "aten::arange", f"with {len(args)} arguments"
        )


def arange(g: jit_utils.GraphContext, *args):
    def _get_arange_dtype(dtype):
        dtype = symbolic_helper._maybe_get_const(dtype, "i")
        return dtype

    def _float_step_convert(range_tensor):
        if symbolic_helper._is_fp(range_tensor):
            range_tensor = g.op(
                "Cast",
                g.op("Ceil", range_tensor),
                to_i=_type_utils.JitScalarType.INT64.onnx_type(),
            )
        return range_tensor

    if len(args) == 2 or len(args) == 5:
        if len(args) == 2:
            # aten::arange(Scalar end, Tensor out)
            dtype = None
        else:
            # aten::arange(Scalar end, ScalarType dtype, Layout, Device, bool pin_memory)
            dtype = _get_arange_dtype(args[1])
        dtype, end, start, step = symbolic_helper._arange_cast_helper(
            g, end=args[0], dtype=dtype
        )
        end = symbolic_helper._unsqueeze_helper(g, end, [0])
        range_tensor = _float_step_convert(end)
        arange_tensor = symbolic_helper._squeeze_helper(
            g, nonzero(g, ones(g, range_tensor, dtype, None, None)), [1]
        )
        return g.op(
            "Cast", arange_tensor, to_i=_type_utils.JitScalarType(dtype).onnx_type()
        )
    elif len(args) == 4 or len(args) == 7:
        if len(args) == 4:
            # aten::arange(Scalar start, Scalar end, Scalar step, Tensor out)
            dtype = None
        else:
            # aten::arange(Scalar start, Scalar end, Scalar step, ScalarType dtype, Layout, Device, bool pin_memory)
            dtype = _get_arange_dtype(args[3])
        dtype, end, start, step = symbolic_helper._arange_cast_helper(
            g, start=args[0], end=args[1], step=args[2], dtype=dtype
        )
        step = symbolic_helper._unsqueeze_helper(g, step, [0])
        end = symbolic_helper._unsqueeze_helper(g, end, [0])
        start = symbolic_helper._unsqueeze_helper(g, start, [0])
        range_tensor = _float_step_convert(g.op("Div", g.op("Sub", end, start), step))
        arange_tensor = symbolic_helper._squeeze_helper(
            g, nonzero(g, ones(g, range_tensor, None, None, None)), [1]
        )
        arange_tensor = g.op("Add", g.op("Mul", arange_tensor, step), start)
        return g.op(
            "Cast", arange_tensor, to_i=_type_utils.JitScalarType(dtype).onnx_type()
        )
    elif len(args) == 6:
        # aten::arange(Scalar start, Scalar end, ScalarType dtype, Layout, Device, bool pin_memory)
        dtype = _get_arange_dtype(args[2])
        dtype, end, start, step = symbolic_helper._arange_cast_helper(
            g, start=args[0], end=args[1], dtype=dtype
        )
        end = symbolic_helper._unsqueeze_helper(g, end, [0])
        start = symbolic_helper._unsqueeze_helper(g, start, [0])
        range_tensor = _float_step_convert(g.op("Sub", end, start))
        arange_tensor = g.op(
            "Add",
            symbolic_helper._squeeze_helper(
                g, nonzero(g, ones(g, range_tensor, dtype, *(args[3:]))), [1]
            ),
            start,
        )
        return g.op(
            "Cast", arange_tensor, to_i=_type_utils.JitScalarType(dtype).onnx_type()
        )

    return symbolic_helper._unimplemented("aten::arange", f"with {len(args)} arguments")


def arange(
    start: float,
    /,
    stop: float | None = None,
    step: float = 1,
    *,
    xp: Namespace,
    dtype: DType | None = None,
    device: Device | None = None,
    **kwargs: object,
) -> Array:
    _check_device(xp, device)
    return xp.arange(start, stop=stop, step=step, dtype=dtype, **kwargs)


def arange(start: float,
           /,
           stop: float | None = None,
           step: float = 1,
           *,
           dtype: DType | None = None,
           device: Device | None = None,
           **kwargs: object) -> Array:
    if stop is None:
        start, stop = 0, start
    if step > 0 and stop <= start or step < 0 and stop >= start:
        if dtype is None:
            if _builtin_all(isinstance(i, int) for i in [start, stop, step]):
                dtype = torch.int64
            else:
                dtype = torch.float32
        return torch.empty(0, dtype=dtype, device=device, **kwargs)
    return torch.arange(start, stop, step, dtype=dtype, device=device, **kwargs)


def arange(
    start: float,
    /,
    stop: float | None = None,
    step: float = 1,
    *,
    dtype: DType | None = None,
    device: Device | None = None,
    **kwargs: object,
) -> Array:
    """
    Array API compatibility wrapper for arange().

    See the corresponding documentation in the array library and/or the array API
    specification for more details.
    """
    # TODO: respect device keyword?
    _helpers._check_device(da, device)

    args: list[Any] = [start]
    if stop is not None:
        args.append(stop)
    else:
        # stop is None, so start is actually stop
        # prepend the default value for start which is 0
        args.insert(0, 0)
    args.append(step)

    return da.arange(*args, dtype=dtype, **kwargs)


def arange(start: ArrayLike | DimSize, stop: ArrayLike | DimSize | None = None,
           step: ArrayLike | None = None, dtype: DTypeLike | None = None,
           *, device: xc.Device | Sharding | None = None,
           out_sharding: NamedSharding | P | None = None) -> Array:
  """Create an array of evenly-spaced values.

  JAX implementation of :func:`numpy.arange`, implemented in terms of
  :func:`jax.lax.iota`.

  Similar to Python's :func:`range` function, this can be called with a few
  different positional signatures:

  - ``jnp.arange(stop)``: generate values from 0 to ``stop``, stepping by 1.
  - ``jnp.arange(start, stop)``: generate values from ``start`` to ``stop``,
    stepping by 1.
  - ``jnp.arange(start, stop, step)``: generate values from ``start`` to ``stop``,
    stepping by ``step``.

  Like with Python's :func:`range` function, the starting value is inclusive,
  and the stop value is exclusive.

  Args:
    start: start of the interval, inclusive.
    stop: optional end of the interval, exclusive. If not specified, then
      ``(start, stop) = (0, start)``
    step: optional step size for the interval. Default = 1.
    dtype: optional dtype for the returned array; if not specified it will
      be determined via type promotion of `start`, `stop`, and `step`.
    device: (optional) :class:`~jax.Device` or :class:`~jax.sharding.Sharding`
      to which the created array will be committed.
    out_sharding: (optional) :class:`~jax.NamedSharding` or :class:`~jax.P` to
      which the created array will be committed. Use `out_sharding` argument,
      if using explicit sharding
      (https://docs.jax.dev/en/latest/parallel.html)

  Returns:
    Array of evenly-spaced values from ``start`` to ``stop``, separated by ``step``.

  Note:
    Using ``arange`` with a floating-point ``step`` argument can lead to unexpected
    results due to accumulation of floating-point errors, especially with
    lower-precision data types like ``float8_*`` and ``bfloat16``.
    To avoid precision errors, consider generating a range of integers, and scaling
    it to the desired range. For example, instead of this::

       jnp.arange(-1, 1, 0.01, dtype='bfloat16')

    it can be more accurate to generate a sequence of integers, and scale them::

       (jnp.arange(-100, 100) * 0.01).astype('bfloat16')

  Examples:
    Single-argument version specifies only the ``stop`` value:

    >>> jnp.arange(4)
    Array([0, 1, 2, 3], dtype=int32)

    Passing a floating-point ``stop`` value leads to a floating-point result:

    >>> jnp.arange(4.0)
    Array([0., 1., 2., 3.], dtype=float32)

    Two-argument version specifies ``start`` and ``stop``, with ``step=1``:

    >>> jnp.arange(1, 6)
    Array([1, 2, 3, 4, 5], dtype=int32)

    Three-argument version specifies ``start``, ``stop``, and ``step``:

    >>> jnp.arange(0, 2, 0.5)
    Array([0. , 0.5, 1. , 1.5], dtype=float32)

  See Also:
    - :func:`jax.numpy.linspace`: generate a fixed number of evenly-spaced values.
    - :func:`jax.lax.iota`: directly generate integer sequences in XLA.
  """
  sharding = util.choose_device_or_out_sharding(
      device, out_sharding, 'jnp.arange')
  if sharding is None or not sharding._is_concrete:
    assert sharding is None or isinstance(sharding, NamedSharding)
    return _arange(start, stop=stop, step=step, dtype=dtype,
                   out_sharding=sharding)
  else:
    output = _arange(start, stop=stop, step=step, dtype=dtype)
    return api.device_put(output, sharding)

