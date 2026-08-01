
def zeros_like(
    self,
    dtype=None,
    layout=None,
    device=None,
    pin_memory=None,
    memory_format=None,
):
    if layout == torch.sparse_coo:
        torch._check(
            memory_format is None,
            lambda: "memory format option is only supported by strided tensors",
        )

        res = torch.empty(
            0,
            dtype=self.dtype if dtype is None else dtype,
            layout=layout,
            device=self.device if device is None else device,
            pin_memory=pin_memory,
        )

        if self.is_sparse:
            res.sparse_resize_and_clear_(
                self.size(), self.sparse_dim(), self.dense_dim()
            )
        else:
            res.sparse_resize_and_clear_(self.size(), self.dim(), 0)

        res._coalesced_(True)
        return res
    res = aten.empty_like.default(
        self,
        dtype=dtype,
        layout=layout,
        device=device,
        pin_memory=pin_memory,
        memory_format=memory_format,
    )
    # device can be not "meta"
    res.fill_(0)
    return res


def zeros_like(
    a: ArrayLike,
    dtype: DTypeLike | None = None,
    order: NotImplementedType = "K",
    subok: NotImplementedType = False,
    shape=None,
):
    result = torch.zeros_like(a, dtype=dtype)
    if shape is not None:
        result = result.reshape(shape)
    return result


def zeros_like(
    a: TensorLikeType,
    *,
    dtype: torch.dtype | None = None,
    layout: torch.layout | None = None,
    device: DeviceLikeType | None = None,
    pin_memory: bool = False,
    requires_grad: bool = False,
    memory_format: torch.memory_format = torch.preserve_format,
) -> TensorLikeType:
    return torch.full_like(
        a,
        False if (dtype or a.dtype) == torch.bool else 0,
        dtype=dtype,
        layout=layout,
        device=device,
        pin_memory=pin_memory,
        requires_grad=requires_grad,
        memory_format=memory_format,
    )


def zeros_like(
    g: jit_utils.GraphContext,
    input,
    dtype,
    layout,
    device,
    pin_memory=False,
    memory_format=None,
):
    shape = g.op("Shape", input)
    return _constant_fill(g, shape, dtype, 0)


def zeros_like(
    g: jit_utils.GraphContext,
    input,
    dtype=None,
    layout=None,
    device=None,
    pin_memory=False,
    memory_format=None,
):
    shape = g.op("Shape", input)
    if symbolic_helper._is_none(dtype):
        scalar_type = _type_utils.JitScalarType.from_value(
            input, _type_utils.JitScalarType.FLOAT
        )
    else:
        # pyrefly: ignore [bad-argument-type]
        scalar_type = _type_utils.JitScalarType(dtype)
    return g.op(
        "ConstantOfShape",
        shape,
        value_t=torch.tensor([0], dtype=scalar_type.dtype()),
    )


def zeros_like(
    x: Array,
    /,
    xp: Namespace,
    *,
    dtype: DType | None = None,
    device: Device | None = None,
    **kwargs: object,
) -> Array:
    _check_device(xp, device)
    return xp.zeros_like(x, dtype=dtype, **kwargs)


def zeros_like(
    a, dtype=None, order='K', subok=True, shape=None, *, device=None
):
    """
    Return an array of zeros with the same shape and type as a given array.

    Parameters
    ----------
    a : array_like
        The shape and data-type of `a` define these same attributes of
        the returned array.
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
        Array of zeros with the same shape and type as `a`.

    See Also
    --------
    empty_like : Return an empty array with shape and type of input.
    ones_like : Return an array of ones with shape and type of input.
    full_like : Return a new array with shape of input filled with value.
    zeros : Return a new array setting values to zero.

    Examples
    --------
    >>> import numpy as np
    >>> x = np.arange(6)
    >>> x = x.reshape((2, 3))
    >>> x
    array([[0, 1, 2],
           [3, 4, 5]])
    >>> np.zeros_like(x)
    array([[0, 0, 0],
           [0, 0, 0]])

    >>> y = np.arange(3, dtype=np.float64)
    >>> y
    array([0., 1., 2.])
    >>> np.zeros_like(y)
    array([0.,  0.,  0.])

    """
    res = empty_like(
        a, dtype=dtype, order=order, subok=subok, shape=shape, device=device
    )
    # needed instead of a 0 to get same result as zeros for string dtypes
    z = zeros(1, dtype=res.dtype)
    multiarray.copyto(res, z, casting='unsafe')
    return res


def zeros_like(a: ArrayLike | DuckTypedArray,
               dtype: DTypeLike | None = None,
               shape: Any = None, *,
               device: xc.Device | Sharding | None = None,
               out_sharding: NamedSharding | P | None = None) -> Array:
  """Create an array full of zeros with the same shape and dtype as an array.

  JAX implementation of :func:`numpy.zeros_like`.

  Args:
    a: Array-like object with ``shape`` and ``dtype`` attributes.
    shape: optionally override the shape of the created array.
    dtype: optionally override the dtype of the created array.
    device: (optional) :class:`~jax.Device` or :class:`~jax.sharding.Sharding`
      to which the created array will be committed.

  Returns:
    Array of the specified shape and dtype, on the specified device if specified.

  See also:
    - :func:`jax.numpy.zeros`
    - :func:`jax.numpy.empty_like`
    - :func:`jax.numpy.ones_like`
    - :func:`jax.numpy.full_like`

  Examples:
    >>> x = jnp.arange(4)
    >>> jnp.zeros_like(x)
    Array([0, 0, 0, 0], dtype=int32)
    >>> jnp.zeros_like(x, dtype=bool)
    Array([False, False, False, False], dtype=bool)
    >>> jnp.zeros_like(x, shape=(2, 3))
    Array([[0, 0, 0],
           [0, 0, 0]], dtype=int32)
  """
  if not (hasattr(a, 'dtype') and hasattr(a, 'shape')):  # support duck typing
    m = getattr(a, '__jax_array__', None)
    if m is not None:
      a = m()
    util.check_arraylike("zeros_like", a)
  if dtype is not None:
    dtype = dtypes.check_and_canonicalize_user_dtype(dtype, "zeros_like")
  if shape is not None:
    shape = canonicalize_shape(shape)
  sharding = util.choose_device_or_out_sharding(
      device, out_sharding, "jnp.zeros_like")
  return lax.full_like(a, 0, dtype, shape, sharding=sharding)

