
def full_like(
    self: torch.Tensor,
    fill_value: int | float,
    *,
    dtype: torch.dtype | None = None,
    layout: torch.layout | None = None,
    device: torch.device | None = None,
    pin_memory: bool = False,
    requires_grad: bool = False,
    memory_format: torch.memory_format = torch.preserve_format,
) -> torch.Tensor:
    dtype = self.dtype if dtype is None else dtype
    layout = self.layout if layout is None else layout
    device = self.device if device is None else device

    if memory_format != torch.preserve_format:
        result = torch.full(
            self.shape,
            fill_value,
            dtype=dtype,
            layout=layout,
            device=device,
            pin_memory=pin_memory,
            requires_grad=requires_grad,
        )
        return result.to(memory_format=memory_format)

    else:
        assert layout == torch.strided
        shape, permutation = _get_shape_permutation_like(self)
        result = torch.full(
            shape,
            fill_value,
            dtype=dtype,
            layout=layout,
            device=device,
            pin_memory=pin_memory,
            requires_grad=requires_grad,
        )
        if permutation == list(range(len(permutation))):
            return result
        return result.permute(permutation).clone()


def full_like(x, fill_value, **kwargs):
    return create_tensor_like(tensor_constructor(fill_value))(x, **kwargs)


def full_like(
    a: ArrayLike,
    fill_value,
    dtype: DTypeLike | None = None,
    order: NotImplementedType = "K",
    subok: NotImplementedType = False,
    shape=None,
):
    # XXX: fill_value broadcasts
    result = torch.full_like(a, fill_value, dtype=dtype)
    if shape is not None:
        result = result.reshape(shape)
    return result


def full_like(
    a: TensorLikeType,
    fill_value: NumberType,
    *,
    dtype: torch.dtype | None = None,
    layout: torch.layout | None = None,
    device: DeviceLikeType | None = None,
    pin_memory: bool = False,
    requires_grad: bool = False,
    memory_format: torch.memory_format = torch.preserve_format,
) -> TensorLikeType:
    e = torch.empty_like(
        a,
        dtype=dtype,
        layout=layout,
        device=device,
        pin_memory=pin_memory,
        requires_grad=requires_grad,
        memory_format=memory_format,
    )
    return fill(e, fill_value)


def full_like(
    g: jit_utils.GraphContext,
    input,
    fill_value,
    dtype,
    layout,
    device,
    pin_memory=False,
    memory_format=None,
):
    shape = g.op("Shape", input)
    return _constant_fill(g, shape, dtype, fill_value)


def full_like(
    g: jit_utils.GraphContext,
    input,
    fill_value,
    dtype=None,
    layout=None,
    device=None,
    pin_memory=False,
    memory_format=None,
):
    fill_value = symbolic_helper._maybe_get_const(fill_value, "f")
    dtype = symbolic_helper._get_const(dtype, "i", "dtype")
    if dtype is None:
        scalar_type = _type_utils.JitScalarType.from_value(
            input, _type_utils.JitScalarType.FLOAT
        )
    else:
        scalar_type = _type_utils.JitScalarType(dtype)
    if symbolic_helper._is_value(fill_value):
        tmp = zeros_like(g, input, dtype, layout, device)
        fill_value = g.op("Cast", fill_value, to_i=scalar_type.onnx_type())
        return add(g, tmp, fill_value, g.op("Constant", value_t=torch.tensor(1)))
    else:
        shape = g.op("Shape", input)
        return g.op(
            "ConstantOfShape",
            shape,
            value_t=torch.tensor([fill_value], dtype=scalar_type.dtype()),
        )


def full_like(
    x: Array,
    /,
    fill_value: complex,
    *,
    xp: Namespace,
    dtype: DType | None = None,
    device: Device | None = None,
    **kwargs: object,
) -> Array:
    _check_device(xp, device)
    return xp.full_like(x, fill_value, dtype=dtype, **kwargs)


def full_like(
    a, fill_value, dtype=None, order='K', subok=True, shape=None,
    *, device=None
):
    """
    Return a full array with the same shape and type as a given array.

    Parameters
    ----------
    a : array_like
        The shape and data-type of `a` define these same attributes of
        the returned array.
    fill_value : array_like
        Fill value.
    dtype : data-type, optional
        Overrides the data type of the result.
    order : {'C', 'F', 'A', or 'K'}, optional
        Overrides the memory layout of the result. 'C' means C-order,
        'F' means F-order, 'A' means 'F' if `a` is Fortran contiguous,
        'C' otherwise. 'K' means match the layout of `a` as closely
        as possible.
    subok : bool, optional.
        If True, then the newly created array will use the sub-class
        type of `a`, otherwise it will be a base-class array. Defaults
        to True.
    shape : int or sequence of ints, optional.
        Overrides the shape of the result. If order='K' and the number of
        dimensions is unchanged, will try to keep order, otherwise,
        order='C' is implied.
    device : str, optional
        The device on which to place the created array. Default: None.
        For Array-API interoperability only, so must be ``"cpu"`` if passed.

        .. versionadded:: 2.0.0

    Returns
    -------
    out : ndarray
        Array of `fill_value` with the same shape and type as `a`.

    See Also
    --------
    empty_like : Return an empty array with shape and type of input.
    ones_like : Return an array of ones with shape and type of input.
    zeros_like : Return an array of zeros with shape and type of input.
    full : Return a new array of given shape filled with value.

    Examples
    --------
    >>> import numpy as np
    >>> x = np.arange(6, dtype=np.int_)
    >>> np.full_like(x, 1)
    array([1, 1, 1, 1, 1, 1])
    >>> np.full_like(x, 0.1)
    array([0, 0, 0, 0, 0, 0])
    >>> np.full_like(x, 0.1, dtype=np.float64)
    array([0.1, 0.1, 0.1, 0.1, 0.1, 0.1])
    >>> np.full_like(x, np.nan, dtype=np.float64)
    array([nan, nan, nan, nan, nan, nan])

    >>> y = np.arange(6, dtype=np.float64)
    >>> np.full_like(y, 0.1)
    array([0.1, 0.1, 0.1, 0.1, 0.1, 0.1])

    >>> y = np.zeros([2, 2, 3], dtype=np.int_)
    >>> np.full_like(y, [0, 0, 255])
    array([[[  0,   0, 255],
            [  0,   0, 255]],
           [[  0,   0, 255],
            [  0,   0, 255]]])
    """
    res = empty_like(
        a, dtype=dtype, order=order, subok=subok, shape=shape, device=device
    )
    multiarray.copyto(res, fill_value, casting='unsafe')
    return res


def full_like(x: ArrayLike | DuckTypedArray,
              fill_value: ArrayLike, dtype: DTypeLike | None = None,
              shape: Shape | None = None, sharding: Sharding | None = None) -> Array:
  """Create a full array like np.full based on the example array `x`.

  Args:
    x: example array-like, used for shape and dtype information.
    fill_value: a scalar value to fill the entries of the output array.
    dtype: optional, a dtype parameter for the output ndarray.
    shape: optional, a shape parameter for the output ndarray.
    sharding: an optional sharding specification for the resulting array.
      If not specified, the output will have the same sharding as the input,
      with a few exceptions/limitations in particular:
      1. Sharding is not available during tracing, thus this will rely on jit.
      2. If x is weakly typed or uncommitted, will use default sharding.
      3. Shape is not None and is different from x.shape, default will be used.

  Returns:
    An ndarray with the same shape as `x` with its entries set equal to
    `fill_value`, similar to the output of np.full.
  """
  fill_shape = np.shape(x) if shape is None else canonicalize_shape(shape)  # pyrefly: ignore[no-matching-overload]
  weak_type = dtype is None and dtypes.is_weakly_typed(x)
  dtype = _dtype(dtype) if dtype is not None else _dtype(x)
  if isinstance(dtype, dtypes.ExtendedDType):
    return dtype._rules.full(fill_shape, fill_value, dtype)

  if sharding is None and shape is None and isinstance(x, core.Tracer):
    sharding = x.aval.sharding  # pyrefly: ignore[missing-attribute]
  else:
    # If `x` has a sharding but no `_committed` attribute
    # (in case of ShapeDtypeStruct), default it to True.
    use_x_sharding = (
        sharding is None
        # Tracer have special logic in handling sharding and even
        # though hasattr(x, 'sharding') returns False, it is very slow.
        # This bypasses the check.
        and not isinstance(x, core.Tracer)
        and hasattr(x, 'sharding')
        and x.sharding is not None
        and (x.sharding._is_concrete or not get_concrete_mesh().empty or
             (isinstance(x.sharding, NamedSharding) and x.sharding.mesh.are_all_axes_explicit))
        and getattr(x, '_committed', True)
        and not weak_type
        and (fill_shape == np.shape(x) or x.sharding.is_fully_replicated)  # pyrefly: ignore[no-matching-overload]
    )
    if use_x_sharding:
      sharding = x.sharding  # pyrefly: ignore[missing-attribute]
  val = full(fill_shape, _convert_element_type(fill_value, dtype, weak_type),
             sharding=sharding)
  val = _full_like_insert_pvary(val, x)
  return val


def full_like(a: ArrayLike | DuckTypedArray,
              fill_value: ArrayLike, dtype: DTypeLike | None = None,
              shape: Any = None, *,
              device: xc.Device | Sharding | None = None,
              out_sharding: NamedSharding | P | None = None) -> Array:
  """Create an array full of a specified value with the same shape and dtype as an array.

  JAX implementation of :func:`numpy.full_like`.

  Args:
    a: Array-like object with ``shape`` and ``dtype`` attributes.
    fill_value: scalar or array with which to fill the created array.
    shape: optionally override the shape of the created array.
    dtype: optionally override the dtype of the created array.
    device: (optional) :class:`~jax.Device` or :class:`~jax.sharding.Sharding`
      to which the created array will be committed.

  Returns:
    Array of the specified shape and dtype, on the specified device if specified.

  See also:
    - :func:`jax.numpy.full`
    - :func:`jax.numpy.empty_like`
    - :func:`jax.numpy.zeros_like`
    - :func:`jax.numpy.ones_like`

  Examples:
    >>> x = jnp.arange(4.0)
    >>> jnp.full_like(x, 2)
    Array([2., 2., 2., 2.], dtype=float32)
    >>> jnp.full_like(x, 0, shape=(2, 3))
    Array([[0., 0., 0.],
           [0., 0., 0.]], dtype=float32)

    `fill_value` may also be an array that is broadcast to the specified shape:

    >>> x = jnp.arange(6).reshape(2, 3)
    >>> jnp.full_like(x, fill_value=jnp.array([[1], [2]]))
    Array([[1, 1, 1],
           [2, 2, 2]], dtype=int32)
  """
  if hasattr(a, 'dtype') and hasattr(a, 'shape'):  # support duck typing
    util.check_arraylike("full_like", 0, fill_value)
  else:
    util.check_arraylike("full_like", a, fill_value)
    m = getattr(a, '__jax_array__', None)
    if m is not None:
      a = m()
  if dtype is not None:
    dtype = dtypes.check_and_canonicalize_user_dtype(dtype, "full_like")
  if shape is not None:
    shape = canonicalize_shape(shape)
  sharding = util.choose_device_or_out_sharding(
      device, out_sharding, 'full_like')
  if np.ndim(fill_value) == 0:
    return lax.full_like(a, fill_value, dtype, shape, sharding=sharding)
  else:
    shape = np.shape(a) if shape is None else shape  # pyrefly: ignore[no-matching-overload]
    dtype = dtypes.result_type(a) if dtype is None else dtype
    if isinstance(sharding, SingleDeviceSharding):
      return api.device_put(
          util._broadcast_to(asarray(fill_value, dtype=dtype), shape), device)
    else:
      return util._broadcast_to(asarray(fill_value, dtype=dtype), shape,
                                sharding=sharding)

