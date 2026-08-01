
def broadcast_to(array: ArrayLike, shape, subok: NotImplementedType = False):
    return torch.broadcast_to(array, size=shape)


def broadcast_to(a: TensorLikeType, size: ShapeType) -> TensorLikeType:
    start = len(size) - len(a.shape)
    dims = tuple(range(start, len(a.shape) + start))
    return prims.broadcast_in_dim(a, size, dims)


def broadcast_to(g: jit_utils.GraphContext, self, size):
    size = symbolic_helper._maybe_get_const(size, "is")
    if not symbolic_helper._is_value(size):
        size = g.op("Constant", value_t=torch.LongTensor(size))
    elif symbolic_helper._is_packed_list(size):
        # Expand with -1 dim value means dim is unchanged.
        # Since onnx::expand supports two-way broadcasting,
        # -1 dim value can be exported to onnx as 1
        size = symbolic_helper._reshape_helper(
            g, stack(g, size, 0), g.op("Constant", value_t=torch.tensor([-1]))
        )
    dtype = _type_utils.JitScalarType.INT64
    ones = ones_like(g, size, dtype)
    neg_ones = mul(g, ones, g.op("Constant", value_t=torch.tensor(-1)))
    size = where(g, g.op("Equal", size, neg_ones), ones, size)
    return g.op("Expand", self, size)


def broadcast_to(func, *args, **kwargs):
    _, new_kwargs = normalize_function(  # type: ignore[misc]
        func, args=args, kwargs=kwargs, normalize_to_only_use_kwargs=True
    )

    inp = new_kwargs.pop("input")
    size = new_kwargs.pop("size")

    if len(size) <= inp.dim():
        return inp.expand([*(1 for _ in range(inp.dim() - len(size))), *size])

    raise ValueError(
        "broadcast_to(): broadcasting to a higher-dim shape is currently not supported "
        "for nested tensors with the jagged layout"
    )


def broadcast_to(x: Array, /, shape: tuple[int, ...], **kwargs: object) -> Array:
    return torch.broadcast_to(x, shape, **kwargs)


def broadcast_to(array, shape, subok=False):
    """Broadcast an array to a new shape.

    Parameters
    ----------
    array : array_like
        The array to broadcast.
    shape : tuple or int
        The shape of the desired array. A single integer ``i`` is interpreted
        as ``(i,)``.
    subok : bool, optional
        If True, then sub-classes will be passed-through, otherwise
        the returned array will be forced to be a base-class array (default).

    Returns
    -------
    broadcast : array
        A readonly view on the original array with the given shape. It is
        typically not contiguous. Furthermore, more than one element of a
        broadcasted array may refer to a single memory location.

    Raises
    ------
    ValueError
        If the array is not compatible with the new shape according to NumPy's
        broadcasting rules.

    See Also
    --------
    broadcast
    broadcast_arrays
    broadcast_shapes

    Examples
    --------
    >>> import numpy as np
    >>> x = np.array([1, 2, 3])
    >>> np.broadcast_to(x, (3, 3))
    array([[1, 2, 3],
           [1, 2, 3],
           [1, 2, 3]])
    """
    return _broadcast_to(array, shape, subok=subok, readonly=True)


def broadcast_to(arr: ArrayLike, shape: Shape,
                 sharding: NamedSharding | None = None) -> Array:
  arr_aval = core.typeof(arr)
  arr_shape = arr_aval.shape
  if (core.definitely_equal_shape(arr_shape, shape) and
      (sharding is None or arr_aval.sharding == sharding)):
    return asarray(arr)
  elif len(shape) < len(arr_shape):
    raise ValueError(
        f"Cannot broadcast to shape with fewer dimensions: {arr_shape=} {shape=}")

  nlead = len(shape) - len(arr_shape)
  shape_tail = shape[nlead:]
  shape_compatible = all(core.definitely_equal_one_of_dim(arr_d, [1, shape_d])
                          for arr_d, shape_d in zip(arr_shape, shape_tail))
  if sharding is None:
    sharding_compatible = True
  else:
    spec_tail = sharding.spec._normalized_spec_for_aval(len(shape))[nlead:]
    sharding_compatible = all(
        arr_s in [None, out_s]
        for arr_s, out_s in zip(arr_aval.sharding.spec, spec_tail))
  if nlead < 0 or not shape_compatible or not sharding_compatible:
    exp_type = core.str_short_aval(
        shape, arr_aval.dtype, None if sharding is None else sharding.mesh,
        P(*[None] * len(shape)) if sharding is None else sharding.spec,
        core.ManualAxisType(), core.MemorySpace.Device)
    raise ValueError(
        f'Incompatible types for broadcasting: input type={arr_aval} and'
        f' requested type={exp_type}')
  return broadcast_in_dim(arr, shape, tuple(range(nlead, len(shape))),
                          out_sharding=sharding)


def broadcast_to(array: ArrayLike, shape: DimSize | Shape,
                 *, out_sharding: NamedSharding | P | None = None) -> Array:
  """Broadcast an array to a specified shape.

  JAX implementation of :func:`numpy.broadcast_to`. JAX uses NumPy-style
  broadcasting rules, which you can read more about at `NumPy broadcasting`_.

  Args:
    array: array to be broadcast.
    shape: shape to which the array will be broadcast.

  Returns:
    a copy of array broadcast to the specified shape.

  See also:
    - :func:`jax.numpy.broadcast_arrays`: broadcast arrays to a common shape.
    - :func:`jax.numpy.broadcast_shapes`: broadcast input shapes to a common shape.

  Examples:
    >>> x = jnp.int32(1)
    >>> jnp.broadcast_to(x, (1, 4))
    Array([[1, 1, 1, 1]], dtype=int32)

    >>> x = jnp.array([1, 2, 3])
    >>> jnp.broadcast_to(x, (2, 3))
    Array([[1, 2, 3],
           [1, 2, 3]], dtype=int32)

    >>> x = jnp.array([[2], [4]])
    >>> jnp.broadcast_to(x, (2, 4))
    Array([[2, 2, 2, 2],
           [4, 4, 4, 4]], dtype=int32)

  .. _NumPy broadcasting: https://numpy.org/doc/stable/user/basics.broadcasting.html
  """
  return util._broadcast_to(array, shape, sharding=out_sharding)


def broadcast_to(a: Array, shape: tuple[int, ...]) -> Array:
  """Broadcasts an array to a new shape.

  Args:
    a: The array to broadcast.
    shape: The desired shape to broadcast to.

  Returns:
    An array of shape ``shape``.

  See Also:
    :func:`jax.numpy.broadcast_to`
  """
  import jax.numpy as jnp  # pyrefly: ignore[missing-import]
  a = jnp.asarray(a)
  if a.shape == shape:
    return a
  return broadcast_to_p.bind(a, shape=shape)

