from typing import Any

def empty(shape, dtype=None, order='C'):
    """Return a new matrix of given shape and type, without initializing entries.

    Parameters
    ----------
    shape : int or tuple of int
        Shape of the empty matrix.
    dtype : data-type, optional
        Desired output data-type.
    order : {'C', 'F'}, optional
        Whether to store multi-dimensional data in row-major
        (C-style) or column-major (Fortran-style) order in
        memory.

    See Also
    --------
    numpy.empty : Equivalent array function.
    matlib.zeros : Return a matrix of zeros.
    matlib.ones : Return a matrix of ones.

    Notes
    -----
    Unlike other matrix creation functions (e.g. `matlib.zeros`,
    `matlib.ones`), `matlib.empty` does not initialize the values of the
    matrix, and may therefore be marginally faster. However, the values
    stored in the newly allocated matrix are arbitrary. For reproducible
    behavior, be sure to set each element of the matrix before reading.

    Examples
    --------
    >>> import numpy.matlib
    >>> np.matlib.empty((2, 2))    # filled with random data
    matrix([[  6.76425276e-320,   9.79033856e-307], # random
            [  7.39337286e-309,   3.22135945e-309]])
    >>> np.matlib.empty((2, 2), dtype=np.int_)
    matrix([[ 6600475,        0], # random
            [ 6586976, 22740995]])

    """
    return ndarray.__new__(matrix, shape, dtype, order=order)


def empty(
    *size,
    names=None,
    dtype=None,
    layout=None,
    device=None,
    pin_memory=None,
    memory_format=None,
):
    assert_nyi(names is None, "named tensors")
    device = decode_device(device)
    if len(size) == 1 and isinstance(size[0], (list, tuple, torch.Size)):
        size = tuple(size[0])
    return empty_strided(
        size, None, dtype=dtype, layout=layout, device=device, pin_memory=pin_memory
    )


def empty(
    shape,
    dtype: DTypeLike | None = None,
    order: NotImplementedType = "C",
    *,
    like: NotImplementedType = None,
):
    if dtype is None:
        dtype = _dtypes_impl.default_dtypes().float_dtype
    return torch.empty(shape, dtype=dtype)


def empty(
    *shape,
    dtype: torch.dtype | None = None,
    layout: torch.layout = torch.strided,
    device: DeviceLikeType | None = None,
    requires_grad: bool = False,
    pin_memory: bool = False,
    memory_format: torch.memory_format = torch.contiguous_format,
) -> TensorLikeType:
    torch._check(
        memory_format != torch.preserve_format,
        lambda: "torch.empty: the Preserve memory format is not supported",
    )

    shape = utils.extract_shape_from_varargs(shape)

    if memory_format == torch.contiguous_format:
        strides = utils.make_contiguous_strides_for(shape)
    elif memory_format == torch.channels_last_3d:
        # pyrefly: ignore [bad-specialization]
        strides = utils.make_channels_last_3d_strides_for(shape)
    else:  # memory_format == torch.channels_last
        torch._check(
            memory_format == torch.channels_last,
            lambda: f"torch.empty: received an unknown memory format {memory_format}!",
        )
        # pyrefly: ignore [bad-specialization]
        strides = utils.make_channels_last_2d_strides_for(shape)

    return torch.empty_strided(
        shape,
        strides,
        dtype=dtype,
        layout=layout,
        device=device,
        pin_memory=pin_memory,
        requires_grad=requires_grad,
    )


def empty(
    g: jit_utils.GraphContext,
    sizes,
    dtype,
    layout,
    device,
    pin_memory=False,
    memory_format=None,
):
    return zeros(g, sizes, dtype, layout, device, pin_memory)


def empty(
    g: jit_utils.GraphContext,
    sizes,
    dtype,
    layout,
    device,
    pin_memory=False,
    memory_format=None,
):
    return zeros(g, sizes, dtype, layout, device, pin_memory)


def empty(  # type: ignore[no-untyped-def]
    *size,
    dtype: torch.dtype | None = None,
    layout: torch.layout = torch.strided,
    requires_grad: bool = False,
    device_mesh: DeviceMesh | None = None,
    placements: Sequence[Placement] | None = None,
) -> DTensor:
    """
    Returns a :class:`DTensor` filled with uninitialized data. The shape of the :class:`DTensor`
    is defined by the variable argument ``size``.

    Args:
        size (int...): a sequence of integers defining the shape of the output :class:`DTensor`.
            Can be a variable number of arguments or a collection like a list or tuple.
            E.g.: empty(1,2,3..) or empty([1,2,3..]) or empty((1,2,3..))

    Keyword args:
        dtype (:class:`torch.dtype`, optional): the desired data type of returned :class:`DTensor`.
            Default: if ``None``, uses a global default (see :func:`torch.set_default_dtype`).\
        layout (:class:`torch.layout`, optional): the desired layout of returned :class:`DTensor`.
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
        torch.empty,
        torch_size,
        dtype=dtype,
        layout=layout,
        requires_grad=requires_grad,
        device_mesh=device_mesh,
        placements=placements,
    )


def empty(
    *size: _int, dtype: _dtype | None = None, device: _device | None = None
) -> torch.Tensor: ...


def empty(
    size: Sequence[_int],
    *,
    dtype: _dtype | None = None,
    device: _device | None = None,
) -> torch.Tensor: ...


def empty(  # type: ignore[misc]
    *size: Any,
    dtype: _dtype | None = None,
    device: _device | None = None,
) -> torch.Tensor:
    r"""
    Similar to :func:`torch.empty()`. The returned tensor can be used by
    :func:`torch._distributed._symmetric_memory.rendezvous()` to establish a
    symmetric memory tensor among participating processes.

    Args:
        size (int...): a sequence of integers defining the shape of the output tensor.
            Can be a variable number of arguments or a collection like a list or tuple.

    Keyword args:
        dtype (:class:`torch.dtype`, optional): the desired data type of returned tensor.
            Default: if ``None``, uses a global default (see :func:`torch.set_default_dtype`).
        device (:class:`torch.device`, optional): the desired device of returned tensor.
            Default: if ``None``, uses the current device for the default tensor type
            (see :func:`torch.set_default_device`). :attr:`device` will be the CPU
            for CPU tensor types and the current CUDA device for CUDA tensor types.
    """
    if len(size) == 1 and isinstance(size[0], Sequence):
        size = tuple(size[0])
    else:
        size = tuple(size)

    if dtype is None:
        dtype = torch.get_default_dtype()

    if device is None:
        device = torch.get_default_device()
    else:
        device = torch.device(device)

    stride = torch._prims_common.make_contiguous_strides_for(size)

    if _should_use_implicit_mempool() and device.type == "cuda":
        # Allocate tensor from an implicit memory pool
        mempool = get_mem_pool(device)
        # TODO: this path can be made device-agnostic if `use_mem_pool` is
        # elevated from torch.cuda to torch accelerator.
        with torch.cuda.use_mem_pool(mempool):
            return _SymmetricMemory.empty_strided_p2p(size, stride, dtype, device)
    else:
        return _SymmetricMemory.empty_strided_p2p(size, stride, dtype, device)


def empty(
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
    Returns a :class:`ShardedTensor` filled with uninitialized data.
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
        memory_format (:class:`torch.memory_format`, optional): the desired memory format of
            returned Tensor. Default: ``torch.contiguous_format``.
        process_group (ProcessGroup, optional): The process group to work on. If None,
            the default process group will be used.
        init_rrefs (bool, optional): Whether or not to initialize
            :class:`torch.distributed.rpc.RRef`s pointing to remote shards.
            Need to initialize the RPC Framework if specified as ``True``.
            Default: ``False``.

    Returns:
        A :class:`ShardedTensor` object on each rank
    """
    return ShardedTensor(
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


def empty(
    shape: int | tuple[int, ...],
    xp: Namespace,
    *,
    dtype: DType | None = None,
    device: Device | None = None,
    **kwargs: object,
) -> Array:
    _check_device(xp, device)
    return xp.empty(shape, dtype=dtype, **kwargs)


def empty(shape: int | tuple[int, ...],
         *,
         dtype: DType | None = None,
         device: Device | None = None,
         **kwargs: object) -> Array:
    return torch.empty(shape, dtype=dtype, device=device, **kwargs)


def empty(shape, dtype, *, out_sharding=None):
  """Create an empty array of possibly uninitialized values.

  This initialization is backend dependent.

  Args:
    shape: int or sequence of ints specifying the shape of the created array.
    dtype: dtype for the created array.
    out_sharding: (optional) :class:`~jax.sharding.PartitionSpec` or
      :class:`~jax.NamedSharding` representing the sharding of the created
      array (see `explicit sharding`_ for more details).

  Returns:
    Uninitialized array of the specified shape, dtype, and sharding.

  Examples:
    >>> lax.empty(3, jnp.float32)  # doctest: +SKIP
    Array([-5.7326739e+29 -7.7323739e+29 -3.14159256e-29], dtype=float32)

  .. _explicit sharding: https://docs.jax.dev/en/latest/parallel.html
  """
  out_sharding = canonicalize_sharding(out_sharding, 'lax.empty')
  return empty_p.bind(shape=shape, dtype=dtype, out_sharding=out_sharding)


def empty(shape: Any, dtype: DTypeLike | None = None, *,
          device: xc.Device | Sharding | None = None,
          out_sharding: NamedSharding | P | None = None) -> Array:
  """Create an empty array.

  JAX implementation of :func:`numpy.empty`.

  .. note::

    For historical reasons, :func:`jax.numpy.empty` is currently equivalent to
    :func:`jax.numpy.zeros`: i.e. it returns a buffer initialized with zeros.
    To create a buffer of uninitialized values, please use :func:`jax.lax.empty`.

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
    - :func:`jax.lax.empty`
    - :func:`jax.numpy.empty_like`
    - :func:`jax.numpy.zeros`
    - :func:`jax.numpy.ones`
    - :func:`jax.numpy.full`

  Examples:
    >>> jnp.empty(4)  # doctest: +SKIP
    Array([0., 0., 0., 0.], dtype=float32)
    >>> jnp.empty((2, 3), dtype=bool)  # doctest: +SKIP
    Array([[False, False, False],
           [False, False, False]], dtype=bool)

  .. _explicit sharding: https://docs.jax.dev/en/latest/parallel.html
  """
  if (m := _check_forgot_shape_tuple("empty", shape, dtype)): raise TypeError(m)
  dtype = dtypes.check_and_canonicalize_user_dtype(
      float if dtype is None else dtype, "empty")
  return zeros(shape, dtype, device=device, out_sharding=out_sharding)


def empty(shape: Sequence[int], dtype: DTypeLike | None=None, index_dtype: DTypeLike = 'int32',
          sparse_format: str = 'bcoo', **kwds) -> JAXSparse:
  """Create an empty sparse array.

  Args:
    shape: sequence of integers giving the array shape.
    dtype: (optional) dtype of the array.
    index_dtype: (optional) dtype of the index arrays.
    format: string specifying the matrix format (e.g. ['bcoo']).
    **kwds: additional keywords passed to the format-specific _empty constructor.
  Returns:
    mat: empty sparse matrix.
  """
  formats = {'bcsr': BCSR, 'bcoo': BCOO, 'coo': COO, 'csr': CSR, 'csc': CSC}
  if sparse_format not in formats:
    raise ValueError(f"sparse_format={sparse_format!r} not recognized; "
                     f"must be one of {list(formats.keys())}")
  cls = formats[sparse_format]
  return cls._empty(tuple(shape), dtype=dtype, index_dtype=index_dtype, **kwds)

