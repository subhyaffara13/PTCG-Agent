
def ones(shape, dtype=None, order='C'):
    """
    Matrix of ones.

    Return a matrix of given shape and type, filled with ones.

    Parameters
    ----------
    shape : {sequence of ints, int}
        Shape of the matrix
    dtype : data-type, optional
        The desired data-type for the matrix, default is np.float64.
    order : {'C', 'F'}, optional
        Whether to store matrix in C- or Fortran-contiguous order,
        default is 'C'.

    Returns
    -------
    out : matrix
        Matrix of ones of given shape, dtype, and order.

    See Also
    --------
    ones : Array of ones.
    matlib.zeros : Zero matrix.

    Notes
    -----
    If `shape` has length one i.e. ``(N,)``, or is a scalar ``N``,
    `out` becomes a single row matrix of shape ``(1,N)``.

    Examples
    --------
    >>> np.matlib.ones((2,3))
    matrix([[1.,  1.,  1.],
            [1.,  1.,  1.]])

    >>> np.matlib.ones(2)
    matrix([[1.,  1.]])

    """
    a = ndarray.__new__(matrix, shape, dtype, order=order)
    a.fill(1)
    return a


def ones(
    shape,
    dtype: DTypeLike | None = None,
    order: NotImplementedType = "C",
    *,
    like: NotImplementedType = None,
):
    if dtype is None:
        dtype = _dtypes_impl.default_dtypes().float_dtype
    return torch.ones(shape, dtype=dtype)


def ones(
    *size,
    dtype: torch.dtype | None = None,
    layout: torch.layout = torch.strided,
    device: DeviceLikeType | None = None,
    pin_memory: bool = False,
    requires_grad: bool = False,
) -> TensorLikeType:
    size = utils.extract_shape_from_varargs(size)

    if dtype is None:
        dtype = torch.get_default_dtype()

    return torch.full(
        size,
        True if dtype == torch.bool else 1,
        dtype=dtype,
        layout=layout,
        device=device,
        pin_memory=pin_memory,
        requires_grad=requires_grad,
    )


def ones(g: jit_utils.GraphContext, sizes, dtype, layout, device, pin_memory=False):
    return _constant_fill(g, sizes, dtype, 1)


def ones(g: jit_utils.GraphContext, sizes, dtype, layout, device, pin_memory=False):
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
        value_t=torch.tensor([1], dtype=scalar_type.dtype()),
    )


def ones(  # type: ignore[no-untyped-def]
    *size,
    dtype: torch.dtype | None = None,
    layout: torch.layout = torch.strided,
    requires_grad: bool = False,
    device_mesh: DeviceMesh | None = None,
    placements: Sequence[Placement] | None = None,
) -> DTensor:
    """
    Returns a :class:`DTensor` filled with the scalar value 1, with the shape defined
    by the variable argument ``size``.

    Args:
        size (int...): a sequence of integers defining the shape of the output :class:`DTensor`.
            Can be a variable number of arguments or a collection like a list or tuple.
            E.g.: ones(1,2,3..) or ones([1,2,3..]) or ones((1,2,3..))

    Keyword args:
        dtype (:class:`torch.dtype`, optional): the desired data type of returned :class:`DTensor`.
            Default: if ``None``, uses a global default (see :func:`torch.set_default_dtype`).
        layout (:class:`torch.layout`, optional): the desired layout of returned DTensor.
            Default: ``torch.strided``.
        requires_grad (bool, optional): If autograd should record operations on the
            returned :class:`DTensor`. Default: ``False``.
        device_mesh: :class:`DeviceMesh` type, contains the mesh info of ranks
        placements: a sequence of :class:`Placement` type: ``Shard``, ``Replicate``

    Returns:
        A :class:`DTensor` object on each rank
    """
    torch_size = normalize_to_torch_size(size)

    return _dtensor_init_helper(
        torch.ones,
        torch_size,
        dtype=dtype,
        layout=layout,
        requires_grad=requires_grad,
        device_mesh=device_mesh,
        placements=placements,
    )


def ones(
    sharding_spec: ShardingSpec,
    *size,
    dtype=None,
    layout=torch.strided,
    requires_grad=False,
    pin_memory=False,
    memory_format=torch.contiguous_format,
    process_group=None,
    init_rrefs=False,
) -> ShardedTensor:
    """
    Returns a :class:`ShardedTensor` with the scalar value 1.
        Needs to be called on all ranks in an SPMD fashion.

    Args:
        sharding_spec (:class:`torch.distributed._shard.sharding_spec.ShardingSpec`): The specification
            describing how to shard the Tensor.
        size (int...): a sequence of integers defining the shape of the output
            tensor. Can be a variable number of arguments or a collection like a list or tuple.

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
    return full(
        sharding_spec,
        size,
        fill_value=1,
        dtype=dtype,
        layout=layout,
        requires_grad=requires_grad,
        pin_memory=pin_memory,
        memory_format=memory_format,
        process_group=process_group,
        init_rrefs=init_rrefs,
    )


def ones(*args, **kwargs):
    """Returns a matrix of ones with ``rows`` rows and ``cols`` columns;
    if ``cols`` is omitted a square matrix will be returned.

    See Also
    ========

    zeros
    eye
    diag
    """

    if 'c' in kwargs:
        kwargs['cols'] = kwargs.pop('c')

    return Matrix.ones(*args, **kwargs)


def ones(
    shape: int | tuple[int, ...],
    xp: Namespace,
    *,
    dtype: DType | None = None,
    device: Device | None = None,
    **kwargs: object,
) -> Array:
    _check_device(xp, device)
    return xp.ones(shape, dtype=dtype, **kwargs)


def ones(shape: int | tuple[int, ...],
         *,
         dtype: DType | None = None,
         device: Device | None = None,
         **kwargs: object) -> Array:
    return torch.ones(shape, dtype=dtype, device=device, **kwargs)


def ones(shape, dtype=None, order='C', *, device=None, like=None):
    """
    Return a new array of given shape and type, filled with ones.

    Parameters
    ----------
    shape : int or sequence of ints
        Shape of the new array, e.g., ``(2, 3)`` or ``2``.
    dtype : data-type, optional
        The desired data-type for the array, e.g., `numpy.int8`.  Default is
        `numpy.float64`.
    order : {'C', 'F'}, optional, default: C
        Whether to store multi-dimensional data in row-major
        (C-style) or column-major (Fortran-style) order in
        memory.
    device : str, optional
        The device on which to place the created array. Default: None.
        For Array-API interoperability only, so must be ``"cpu"`` if passed.

        .. versionadded:: 2.0.0
    ${ARRAY_FUNCTION_LIKE}

        .. versionadded:: 1.20.0

    Returns
    -------
    out : ndarray
        Array of ones with the given shape, dtype, and order.

    See Also
    --------
    ones_like : Return an array of ones with shape and type of input.
    empty : Return a new uninitialized array.
    zeros : Return a new array setting values to zero.
    full : Return a new array of given shape filled with value.

    Examples
    --------
    >>> import numpy as np
    >>> np.ones(5)
    array([1., 1., 1., 1., 1.])

    >>> np.ones((5,), dtype=np.int_)
    array([1, 1, 1, 1, 1])

    >>> np.ones((2, 1))
    array([[1.],
           [1.]])

    >>> s = (2,2)
    >>> np.ones(s)
    array([[1.,  1.],
           [1.,  1.]])

    """
    if like is not None:
        return _ones_with_like(
            like, shape, dtype=dtype, order=order, device=device
        )

    a = empty(shape, dtype, order, device=device)
    multiarray.copyto(a, 1, casting='unsafe')
    return a


def ones(key: Array,
         shape: core.Shape,
         dtype: DTypeLikeInexact | None = None,
         out_sharding: OutShardingType = None) -> Array:
  """An initializer that returns a constant array full of ones.

  The ``key`` argument is ignored.

  >>> import jax, jax.numpy as jnp
  >>> jax.nn.initializers.ones(jax.random.key(42), (3, 2), jnp.float32)
  Array([[1., 1.],
         [1., 1.],
         [1., 1.]], dtype=float32)
  """
  dtype = dtypes.default_float_dtype() if dtype is None else dtype
  return jnp.ones(shape, dtype, out_sharding=out_sharding)


def ones(shape: Any, dtype: DTypeLike | None = None, *,
         device: xc.Device | Sharding | None = None,
         out_sharding: NamedSharding | P | None = None) -> Array:
  """Create an array full of ones.

  JAX implementation of :func:`numpy.ones`.

  Args:
    shape: int or sequence of ints specifying the shape of the created array.
    dtype: optional dtype for the created array; defaults to float32 or float64
      depending on the X64 configuration (see :ref:`default-dtypes`).
    device: (optional) :class:`~jax.Device` or :class:`~jax.sharding.Sharding`
      to which the created array will be committed. This argument exists for
      compatibility with the :ref:`python-array-api`.
    out_sharding: (optional) :class:`~jax.sharding.PartitionSpec` or :class:`~jax.NamedSharding`
      representing the sharding of the created array (see `explicit sharding`_ for more details).
      This argument exists for consistency with other array creation routines across JAX.
      Specifying both ``out_sharding`` and ``device`` will result in an error.

  Returns:
    Array of the specified shape and dtype, with the given device/sharding if specified.

  See also:
    - :func:`jax.numpy.ones_like`
    - :func:`jax.numpy.empty`
    - :func:`jax.numpy.zeros`
    - :func:`jax.numpy.full`

  Examples:
    >>> jnp.ones(4)
    Array([1., 1., 1., 1.], dtype=float32)
    >>> jnp.ones((2, 3), dtype=bool)
    Array([[ True,  True,  True],
           [ True,  True,  True]], dtype=bool)

  .. _explicit sharding: https://docs.jax.dev/en/latest/parallel.html
  """
  if isinstance(shape, types.GeneratorType):
    raise TypeError("expected sequence object with len >= 0 or a single integer")
  if (m := _check_forgot_shape_tuple("ones", shape, dtype)): raise TypeError(m)
  shape = canonicalize_shape(shape)
  dtype = dtypes.check_and_canonicalize_user_dtype(
      float if dtype is None else dtype, "ones")
  sharding = util.choose_device_or_out_sharding(
      device, out_sharding, 'jnp.ones')
  return lax.full(shape, 1, dtype, sharding=sharding)

