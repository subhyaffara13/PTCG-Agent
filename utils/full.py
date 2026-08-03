from typing import Any

def full(size, fill_value, *args, **kwargs):
    dtype = kwargs.get("dtype")
    if not dtype:
        dtype = utils.get_dtype(fill_value)
    kwargs["dtype"] = dtype

    return torch.empty(size, *args, **kwargs)


def full(
    size: list[int | torch.SymInt],
    fill_value: torch.types.Number,
    **kwargs: Any,
) -> torch.Tensor:
    dtype = kwargs.get("dtype")
    if dtype is None:
        kwargs["dtype"] = type_to_dtype(type(fill_value))
        return torch.full(size, fill_value, **kwargs)
    return NotImplemented


def full(size, fill_value, **kwargs):
    assert kwargs.get("dtype") is not None, "dtype should be handled by decomposition"
    return tensor_constructor(fill_value)(size, **kwargs)


def full(
    shape,
    fill_value: ArrayLike,
    dtype: DTypeLike | None = None,
    order: NotImplementedType = "C",
    *,
    like: NotImplementedType = None,
):
    if isinstance(shape, int):
        shape = (shape,)
    if dtype is None:
        dtype = fill_value.dtype
    if not isinstance(shape, (tuple, list)):
        shape = (shape,)
    return torch.full(shape, fill_value, dtype=dtype)


def full(
    shape: ShapeType,
    fill_value: NumberType,
    *,
    dtype: torch.dtype | None = None,
    layout: torch.layout = torch.strided,
    device: DeviceLikeType | None = None,
    pin_memory: bool = False,
    requires_grad: bool = False,
) -> TensorLikeType:
    utils.check_layout(layout)
    utils.check_pin_memory(pin_memory)

    dtype = dtype if dtype is not None else utils.type_to_dtype(type(fill_value))
    device = device if device is not None else torch.device("cpu")

    e = empty(
        shape,
        dtype=dtype,
        layout=layout,
        device=device,
        pin_memory=pin_memory,
        requires_grad=requires_grad,
    )
    return torch.fill(e, fill_value)  # type: ignore[arg-type]


def full(
    g: jit_utils.GraphContext, sizes, value, dtype, layout, device, pin_memory=False
):
    const_value = symbolic_helper._maybe_get_const(value, "t")
    if symbolic_helper._is_value(const_value):
        tmp = zeros(g, sizes, dtype, layout, device)
        return opset9.add(g, tmp, value, g.op("Constant", value_t=torch.tensor(1)))
    else:
        dtype = symbolic_helper._get_const(dtype, "i", "dtype")
        return _constant_fill(g, sizes, dtype, const_value)


def full(
    g: jit_utils.GraphContext, sizes, value, dtype, layout, device, pin_memory=False
):
    const_value = symbolic_helper._maybe_get_const(value, "t")
    if symbolic_helper._is_value(const_value):
        dtype = _type_utils.JitScalarType.FLOAT if dtype is None else dtype
        tmp = zeros(g, sizes, dtype, layout, device)
        return add(g, tmp, value, g.op("Constant", value_t=torch.tensor(1)))
    else:
        dtype = symbolic_helper._get_const(dtype, "i", "dtype")
        if dtype is None:
            scalar_type = _type_utils.JitScalarType.FLOAT
        else:
            scalar_type = _type_utils.JitScalarType(dtype)
        sizes_ = symbolic_helper._maybe_get_const(sizes, "is")
        if isinstance(sizes_, list) and len(sizes_) == 0:
            sizes = g.op("Constant", value_t=torch.tensor([]).to(torch.int64))
        return g.op(
            "ConstantOfShape",
            sizes,
            value_t=const_value.view(1).to(scalar_type.dtype()),
        )


def full(  # type: ignore[no-untyped-def]
    size,
    fill_value,
    *,
    dtype: torch.dtype | None = None,
    layout: torch.layout = torch.strided,
    requires_grad: bool = False,
    device_mesh: DeviceMesh | None = None,
    placements: Sequence[Placement] | None = None,
) -> DTensor:
    """
    Returns a :class:`DTensor` filled with ``fill_value`` according to ``device_mesh`` and
    ``placements``, with the shape defined by the argument ``size``.

    Args:
        size (int...): a sequence of integers defining the shape of the output :class:`DTensor`.
            Can be a variable number of arguments or a collection like a list or tuple.
            E.g.: ones(1,2,3..) or ones([1,2,3..]) or ones((1,2,3..))
        fill_value(Scalar): the value to fill the output tensor with.

    Keyword args:
        dtype (:class:`torch.dtype`, optional): the desired data type of returned :class:`DTensor`.
            Default: if ``None``, uses a global default (see :func:`torch.set_default_dtype`).
        layout (:class:`torch.layout`, optional): the desired layout of returned DTensor.
            Default: ``torch.strided``.
        requires_grad (bool, optional): If autograd should record operations on the
            returned :class:`DTensor`. Default: ``False``.
        device_mesh: :class:`DeviceMesh` type, contains the mesh info of ranks.
        placements: a sequence of :class:`Placement` type: ``Shard``, ``Replicate``

    Returns:
        A :class:`DTensor` object on each rank
    """
    torch_size = normalize_to_torch_size(size)

    return _dtensor_init_helper(
        torch.full,
        torch_size,
        fill_value=fill_value,
        dtype=dtype,
        layout=layout,
        requires_grad=requires_grad,
        device_mesh=device_mesh,
        placements=placements,
    )


def full(
    sharding_spec: ShardingSpec,
    size,
    fill_value,
    *,
    dtype=None,
    layout=torch.strided,
    requires_grad=False,
    pin_memory=False,
    memory_format=torch.contiguous_format,
    process_group=None,
    init_rrefs=False,
) -> ShardedTensor:
    """
    Creates a :class:`ShardedTensor` filled with fill_value. The tensor's dtype
        is inferred from fill_value. If dtype is specified, it will override the
        inferred type from fill_value. Needs to be called on all ranks in an SPMD fashion.
    Args:
        sharding_spec (:class:`torch.distributed._sharding_spec.ShardingSpec`): The specification
            describing how to shard the Tensor.
        size (int...):  a list, tuple, or `torch.Size` of integers defining the shape of the
            output tensor.
        fill_value (Scalar) - the value to fill the output tensor with.
    Keyword args:
        dtype (:class:`torch.dtype`, optional): the desired data type of returned tensor.
            Default: if ``None``, uses a global default (see :func:`torch.set_default_dtype`).
        layout (:class:`torch.layout`, optional): the desired layout of returned Tensor.
            Default: ``torch.strided``.
        requires_grad (bool, optional): If autograd should record operations on the
            returned tensor. Default: ``False``.
        pin_memory (bool, optional): If set, returned tensor would be allocated in
            the pinned memory. Works only for CPU tensors. Default: ``False``.
        process_group (ProcessGroup, optional): The process group to work on. If None,
            the default process group will be used.
        init_rrefs (bool, optional): Whether or not to initialize
            :class:`torch.distributed.rpc.RRef`s pointing to remote shards.
            Need to initialize the RPC Framework if specified as ``True``.
            Default: ``False``.
    Returns:
        A :class:`ShardedTensor` object on each rank
    """
    sharded_tensor = ShardedTensor(
        sharding_spec,
        *size,
        dtype=dtype,
        layout=layout,
        requires_grad=requires_grad,
        pin_memory=pin_memory,
        memory_format=memory_format,
        process_group=process_group,
        init_rrefs=init_rrefs,
    )
    torch.nn.init.constant_(sharded_tensor, fill_value)  # type: ignore[arg-type]
    return sharded_tensor


def full(
    shape: int | tuple[int, ...],
    fill_value: complex,
    xp: Namespace,
    *,
    dtype: DType | None = None,
    device: Device | None = None,
    **kwargs: object,
) -> Array:
    _check_device(xp, device)
    return xp.full(shape, fill_value, dtype=dtype, **kwargs)


def full(shape: int | tuple[int, ...],
         fill_value: complex,
         *,
         dtype: DType | None = None,
         device: Device | None = None,
         **kwargs: object) -> Array:
    if isinstance(shape, int):
        shape = (shape,)

    return torch.full(shape, fill_value, dtype=dtype, device=device, **kwargs)


def full(shape, fill_value, dtype=None, order='C', *, device=None, like=None):
    """
    Return a new array of given shape and type, filled with `fill_value`.

    Parameters
    ----------
    shape : int or sequence of ints
        Shape of the new array, e.g., ``(2, 3)`` or ``2``.
    fill_value : scalar or array_like
        Fill value.
    dtype : data-type, optional
        The desired data-type for the array  The default, None, means
         ``np.array(fill_value).dtype``.
    order : {'C', 'F'}, optional
        Whether to store multidimensional data in C- or Fortran-contiguous
        (row- or column-wise) order in memory.
    device : str, optional
        The device on which to place the created array. Default: None.
        For Array-API interoperability only, so must be ``"cpu"`` if passed.

        .. versionadded:: 2.0.0
    ${ARRAY_FUNCTION_LIKE}

        .. versionadded:: 1.20.0

    Returns
    -------
    out : ndarray
        Array of `fill_value` with the given shape, dtype, and order.

    See Also
    --------
    full_like : Return a new array with shape of input filled with value.
    empty : Return a new uninitialized array.
    ones : Return a new array setting values to one.
    zeros : Return a new array setting values to zero.

    Examples
    --------
    >>> import numpy as np
    >>> np.full((2, 2), np.inf)
    array([[inf, inf],
           [inf, inf]])
    >>> np.full((2, 2), 10)
    array([[10, 10],
           [10, 10]])

    >>> np.full((2, 2), [1, 2])
    array([[1, 2],
           [1, 2]])

    """
    if like is not None:
        return _full_with_like(
            like, shape, fill_value, dtype=dtype, order=order, device=device
        )

    if dtype is None:
        fill_value = asarray(fill_value)
        dtype = fill_value.dtype
    a = empty(shape, dtype, order, device=device)
    multiarray.copyto(a, fill_value, casting='unsafe')
    return a


def full(shape: Shape, fill_value: ArrayLike, dtype: DTypeLike | None = None, *,
         sharding: Sharding | None = None) -> Array:
  """Returns an array of `shape` filled with `fill_value`.

  Args:
    shape: sequence of integers, describing the shape of the output array.
    fill_value: the value to fill the new array with.
    dtype: the type of the output array, or `None`. If not `None`, `fill_value`
      will be cast to `dtype`.
    sharding: an optional sharding specification for the resulting array,
      note, sharding will currently be ignored in jitted mode, this might change
      in the future.
  """
  shape = canonicalize_shape(shape)
  if np.shape(fill_value):
    msg = "full must be called with scalar fill_value, got fill_value.shape {}."
    raise TypeError(msg.format(np.shape(fill_value)))
  if dtype is None:
    weak_type = dtypes.is_weakly_typed(fill_value)
    fill_dtype = _dtype(fill_value)
  else:
    if isinstance(dtype, dtypes.ExtendedDType):
      return dtype._rules.full(shape, fill_value, dtype)
    weak_type = False
    fill_dtype = dtypes.check_and_canonicalize_user_dtype(dtype, "full")
  fill_value = _convert_element_type(fill_value, fill_dtype, weak_type)
  if (sharding is not None and
      isinstance(fill_value, array.ArrayImpl) and sharding._is_concrete):
    broadcast_shape = sharding.shard_shape(shape)
    shard = broadcast(fill_value, broadcast_shape)
    shard = shard.addressable_data(0)
    return array.make_array_from_callback(
        shape, sharding, lambda _: shard, dtype=fill_dtype)

  if sharding is not None and not sharding._is_concrete:
    return broadcast(fill_value, shape, out_sharding=sharding)
  else:
    return broadcast(fill_value, shape)


def full(shape: Any, fill_value: ArrayLike,
         dtype: DTypeLike | None = None, *,
         device: xc.Device | Sharding | None = None,
         out_sharding: NamedSharding | P | None = None) -> Array:
  """Create an array full of a specified value.

  JAX implementation of :func:`numpy.full`.

  Args:
    shape: int or sequence of ints specifying the shape of the created array.
    fill_value: scalar or array with which to fill the created array.
    dtype: optional dtype for the created array; defaults to the dtype of the
      fill value.
    device: (optional) :class:`~jax.Device` or :class:`~jax.sharding.Sharding`
      to which the created array will be committed.

  Returns:
    Array of the specified shape and dtype, on the specified device if specified.

  See also:
    - :func:`jax.numpy.full_like`
    - :func:`jax.numpy.empty`
    - :func:`jax.numpy.zeros`
    - :func:`jax.numpy.ones`

  Examples:
    >>> jnp.full(4, 2, dtype=float)
    Array([2., 2., 2., 2.], dtype=float32)
    >>> jnp.full((2, 3), 0, dtype=bool)
    Array([[False, False, False],
           [False, False, False]], dtype=bool)

    `fill_value` may also be an array that is broadcast to the specified shape:

    >>> jnp.full((2, 3), fill_value=jnp.arange(3))
    Array([[0, 1, 2],
           [0, 1, 2]], dtype=int32)
  """
  if dtype is not None:
    dtype = dtypes.check_and_canonicalize_user_dtype(dtype, "full")
  util.check_arraylike("full", fill_value)

  sharding = util.choose_device_or_out_sharding(device, out_sharding, 'full')

  if np.ndim(fill_value) == 0:
    shape = canonicalize_shape(shape)
    return lax.full(shape, fill_value, dtype, sharding=sharding)
  else:
    if isinstance(sharding, SingleDeviceSharding):
      return api.device_put(
          util._broadcast_to(asarray(fill_value, dtype=dtype), shape), device)
    else:
      return util._broadcast_to(asarray(fill_value, dtype=dtype), shape,
                                sharding=sharding)

