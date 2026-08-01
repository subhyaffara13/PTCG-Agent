
def randn(*args):
    """
    Return a random matrix with data from the "standard normal" distribution.

    `randn` generates a matrix filled with random floats sampled from a
    univariate "normal" (Gaussian) distribution of mean 0 and variance 1.

    Parameters
    ----------
    \\*args : Arguments
        Shape of the output.
        If given as N integers, each integer specifies the size of one
        dimension. If given as a tuple, this tuple gives the complete shape.

    Returns
    -------
    Z : matrix of floats
        A matrix of floating-point samples drawn from the standard normal
        distribution.

    See Also
    --------
    rand, numpy.random.RandomState.randn

    Notes
    -----
    For random samples from the normal distribution with mean ``mu`` and
    standard deviation ``sigma``, use::

        sigma * np.matlib.randn(...) + mu

    Examples
    --------
    >>> np.random.seed(123)
    >>> import numpy.matlib
    >>> np.matlib.randn(1)
    matrix([[-1.0856306]])
    >>> np.matlib.randn(1, 2, 3)
    matrix([[ 0.99734545,  0.2829785 , -1.50629471],
            [-0.57860025,  1.65143654, -2.42667924]])

    Two-by-four matrix of samples from the normal distribution with
    mean 3 and standard deviation 2.5:

    >>> 2.5 * np.matlib.randn((2, 4)) + 3
    matrix([[1.92771843, 6.16484065, 0.83314899, 1.30278462],
            [2.76322758, 6.72847407, 1.40274501, 1.8900451 ]])

    """
    if isinstance(args[0], tuple):
        args = args[0]
    return asmatrix(np.random.randn(*args))


def randn(*args, **kwargs):
    if kwargs.get("generator") is not None:
        return fallback_randn_generator(*args, **kwargs)
    elif config.fallback_random:
        kwargs.pop("generator", None)
        return fallback_randn_default(*args, **kwargs)
    raise AssertionError("should have been handled in replace_random.py")


def randn(*size):
    dtype = _dtypes_impl.default_dtypes().float_dtype
    values = torch.randn(size, dtype=dtype)
    return array_or_scalar(values, return_scalar=size == ())


def randn(
    *shape,
    dtype: torch.dtype | None = None,
    device: DeviceLikeType | None = None,
    layout: torch.layout | None = None,
    requires_grad: bool = False,
    pin_memory: bool = False,
) -> TensorLikeType:
    utils.check_pin_memory(pin_memory)

    shape_ = utils.extract_shape_from_varargs(shape)

    dtype = utils.dtype_or_default(dtype)
    device = utils.device_or_default(device)

    return prims.normal(
        shape_,
        mean=0.0,
        std=1.0,
        dtype=dtype,
        device=device,
        requires_grad=requires_grad,
    )


def randn(seed, offset):
    i1, i2, _, _ = randint4x(seed, offset, PHILOX_N_ROUNDS_DEFAULT)
    u1 = _uint_to_uniform_float(i1)
    u2 = _uint_to_uniform_float(i2)
    n1, _ = _pair_uniform_to_normal(u1, u2)
    return n1


def randn(g: jit_utils.GraphContext, shapes, dtype, *options):
    dtype = symbolic_helper._get_const(dtype, "i", "dtype")
    if dtype is None:
        scalar_type = _type_utils.JitScalarType.FLOAT
    else:
        scalar_type = _type_utils.JitScalarType(dtype)
    shape = symbolic_helper._maybe_get_const(shapes, "is")
    if symbolic_helper._is_value(shape):
        shape_const = g.op(
            "ConstantOfShape",
            shapes,
            value_t=torch.tensor([0], dtype=torch.float),
        )
        return g.op(
            "RandomNormalLike",
            shape_const,
            dtype_i=scalar_type.onnx_type(),
        )
    return g.op(
        "RandomNormal",
        shape_i=shape,
        dtype_i=scalar_type.onnx_type(),
    )


def randn(  # type: ignore[no-untyped-def]
    *size,
    requires_grad: bool = False,
    dtype: torch.dtype | None = None,
    layout: torch.layout = torch.strided,
    device_mesh: DeviceMesh | None = None,
    placements: Sequence[Placement] | None = None,
) -> DTensor:
    """
    Returns a :class:`DTensor` filled with random numbers from a normal distribution
    with mean 0 and variance 1. The shape of the tensor is defined by the variable
    argument ``size``.

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
        device_mesh: :class:`DeviceMesh` type, contains the mesh info of ranks.
        placements: a sequence of :class:`Placement` type: ``Shard``, ``Replicate``

    Returns:
        A :class:`DTensor` object on each rank
    """
    torch_size = normalize_to_torch_size(size)

    return _dtensor_init_helper(
        torch.randn,
        torch_size,
        dtype=dtype,
        layout=layout,
        requires_grad=requires_grad,
        device_mesh=device_mesh,
        placements=placements,
    )


def randn(
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
    Creates a :class:`ShardedTensor` filled with random numbers from a uniform distribution
        with mean `0` and variance `1` (also called standard normal distribution). The shape
        of the tensor is defined by the variable argument `size`. Needs to be called on all ranks
        in an SPMD fashion.

    Args:
        sharding_spec (:class:`torch.distributed._shard.sharding_spec.ShardingSpec`): The specification
            describing how to shard the Tensor.
        size (int...):  a list, tuple, or `torch.Size` of integers defining the shape of the
            output tensor.

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
    torch.nn.init.normal_(sharded_tensor, 0, 1)  # type: ignore[arg-type]
    return sharded_tensor

