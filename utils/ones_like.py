
def ones_like(
    a: ArrayLike,
    dtype: DTypeLike | None = None,
    order: NotImplementedType = "K",
    subok: NotImplementedType = False,
    shape=None,
):
    result = torch.ones_like(a, dtype=dtype)
    if shape is not None:
        result = result.reshape(shape)
    return result


def ones_like(
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
        True if (dtype or a.dtype) == torch.bool else 1,
        dtype=dtype,
        layout=layout,
        device=device,
        pin_memory=pin_memory,
        requires_grad=requires_grad,
        memory_format=memory_format,
    )


def ones_like(
    g: jit_utils.GraphContext,
    input,
    dtype,
    layout,
    device,
    pin_memory=False,
    memory_format=None,
):
    shape = g.op("Shape", input)
    return _constant_fill(g, shape, dtype, 1)


def ones_like(
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
        value_t=torch.tensor([1], dtype=scalar_type.dtype()),
    )


def ones_like(func, *args, **kwargs):
    _check_args_kwargs_length(args, kwargs, f"__torch_dispatch__, {func}", len_args=1)
    result_data = func(_get_data(args[0]), **kwargs)
    return MaskedTensor(result_data, _maybe_get_mask(args[0]))


def ones_like(
    x: Array,
    /,
    xp: Namespace,
    *,
    dtype: DType | None = None,
    device: Device | None = None,
    **kwargs: object,
) -> Array:
    _check_device(xp, device)
    return xp.ones_like(x, dtype=dtype, **kwargs)


def ones_like(
    a, dtype=None, order='K', subok=True, shape=None, *, device=None
):
    """
    Return an array of ones with the same shape and type as a given array.

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
        Array of ones with the same shape and type as `a`.

    See Also
    --------
    empty_like : Return an empty array with shape and type of input.
    zeros_like : Return an array of zeros with shape and type of input.
    full_like : Return a new array with shape of input filled with value.
    ones : Return a new array setting values to one.

    Examples
    --------
    >>> import numpy as np
    >>> x = np.arange(6)
    >>> x = x.reshape((2, 3))
    >>> x
    array([[0, 1, 2],
           [3, 4, 5]])
    >>> np.ones_like(x)
    array([[1, 1, 1],
           [1, 1, 1]])

    >>> y = np.arange(3, dtype=np.float64)
    >>> y
    array([0., 1., 2.])
    >>> np.ones_like(y)
    array([1.,  1.,  1.])

    """
    res = empty_like(
        a, dtype=dtype, order=order, subok=subok, shape=shape, device=device
    )
    multiarray.copyto(res, 1, casting='unsafe')
    return res


def ones_like(a: ArrayLike | DuckTypedArray,
              dtype: DTypeLike | None = None,
              shape: Any = None, *,
              device: xc.Device | Sharding | None = None,
              out_sharding: NamedSharding | P | None = None) -> Array:
  """Create an array of ones with the same shape and dtype as an array.

  JAX implementation of :func:`numpy.ones_like`.

  Args:
    a: Array-like object with ``shape`` and ``dtype`` attributes.
    shape: optionally override the shape of the created array.
    dtype: optionally override the dtype of the created array.
    device: (optional) :class:`~jax.Device` or :class:`~jax.sharding.Sharding`
      to which the created array will be committed.

  Returns:
    Array of the specified shape and dtype, on the specified device if specified.

  See also:
    - :func:`jax.numpy.empty`
    - :func:`jax.numpy.zeros_like`
    - :func:`jax.numpy.ones_like`
    - :func:`jax.numpy.full_like`

  Examples:
    >>> x = jnp.arange(4)
    >>> jnp.ones_like(x)
    Array([1, 1, 1, 1], dtype=int32)
    >>> jnp.ones_like(x, dtype=bool)
    Array([ True,  True,  True,  True], dtype=bool)
    >>> jnp.ones_like(x, shape=(2, 3))
    Array([[1, 1, 1],
           [1, 1, 1]], dtype=int32)
  """
  if not (hasattr(a, 'dtype') and hasattr(a, 'shape')):  # support duck typing
    m = getattr(a, '__jax_array__', None)
    if m is not None:
      a = m()
    util.check_arraylike("ones_like", a)
  if dtype is not None:
    dtype = dtypes.check_and_canonicalize_user_dtype(dtype, "ones_like")
  if shape is not None:
    shape = canonicalize_shape(shape)
  sharding = util.choose_device_or_out_sharding(
      device, out_sharding, "jnp.ones_like")
  return lax.full_like(a, 1, dtype, shape, sharding=sharding)

