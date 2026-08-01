
def atleast_1d(*tensors):
    r"""
    Returns a 1-dimensional view of each input tensor with zero dimensions.
    Input tensors with one or more dimensions are returned as-is.

    Args:
        input (Tensor or sequence of Tensors): tensor(s) to be converted to at least 1-dimensional.

    Returns:
        output (Tensor or tuple of Tensors)

    Example::

        >>> x = torch.arange(2)
        >>> x
        tensor([0, 1])
        >>> torch.atleast_1d(x)
        tensor([0, 1])
        >>> x = torch.tensor(1.)
        >>> x
        tensor(1.)
        >>> torch.atleast_1d(x)
        tensor([1.])
        >>> x = torch.tensor(0.5)
        >>> y = torch.tensor(1.)
        >>> torch.atleast_1d((x, y))
        (tensor([0.5000]), tensor([1.]))
        >>> torch.atleast_1d()
        ()
    """
    # This wrapper exists to support variadic args.
    if has_torch_function(tensors):
        return handle_torch_function(atleast_1d, tensors, *tensors)
    if len(tensors) == 1:
        tensors = tensors[0]
    return _VF.atleast_1d(tensors)  # type: ignore[attr-defined]


def atleast_1d(tensor_or_array: torch.Tensor | np.ndarray):
    if isinstance(tensor_or_array, torch.Tensor):
        tensor_or_array = torch.atleast_1d(tensor_or_array)
    else:
        tensor_or_array = np.atleast_1d(tensor_or_array)
    return tensor_or_array


def atleast_1d(*arys: ArrayLike):
    res = torch.atleast_1d(*arys)
    if isinstance(res, tuple):
        return list(res)
    else:
        return res


def atleast_1d(
    arg: TensorLikeType | Sequence[TensorLikeType], *args: TensorLikeType
) -> TensorLikeType | tuple[TensorLikeType, ...]:
    """Reference implementation of :func:`torch.atleast_1d`."""
    if not args and isinstance(arg, collections.abc.Sequence):
        args_ = arg
    else:
        if isinstance(arg, collections.abc.Sequence):
            raise AssertionError("arg should not be a Sequence when args is provided")
        args_ = (arg,) + args
    res = tuple(a if a.ndim >= 1 else unsqueeze(a, 0) for a in args_)
    return res if len(res) > 1 else res[0]


def atleast_1d(g: jit_utils.GraphContext, self: torch._C.Value):
    # NOTE: If it's 0D, reshape to 1D

    # NOTE: self could be a packed list or a tensor
    if symbolic_helper._is_value(self) and symbolic_helper._is_packed_list(self):
        tensor_list = symbolic_helper._unpack_list(self)
        new_tensor_list = []
        for tensor in tensor_list:
            new_tensor = tensor
            tensor_rank = symbolic_helper._get_tensor_rank(tensor)
            if tensor_rank == 0:
                new_tensor = symbolic_helper._reshape_helper(
                    g, new_tensor, g.op("Constant", value_t=torch.tensor([1]))
                )
            new_tensor_list.append(new_tensor)
        return g.op("SequenceConstruct", *new_tensor_list)

    tensor_rank = symbolic_helper._get_tensor_rank(self)
    if tensor_rank == 0:
        self = symbolic_helper._reshape_helper(
            g, self, g.op("Constant", value_t=torch.tensor([1]))
        )
    return self


def atleast_1d(*arys):
    """
    Convert inputs to arrays with at least one dimension.

    Scalar inputs are converted to 1-dimensional arrays, whilst
    higher-dimensional inputs are preserved.

    Parameters
    ----------
    arys1, arys2, ... : array_like
        One or more input arrays.

    Returns
    -------
    ret : ndarray
        An array, or tuple of arrays, each with ``a.ndim >= 1``.
        Copies are made only if necessary.

    See Also
    --------
    atleast_2d, atleast_3d

    Examples
    --------
    >>> import numpy as np
    >>> np.atleast_1d(1.0)
    array([1.])

    >>> x = np.arange(9.0).reshape(3,3)
    >>> np.atleast_1d(x)
    array([[0., 1., 2.],
           [3., 4., 5.],
           [6., 7., 8.]])
    >>> np.atleast_1d(x) is x
    True

    >>> np.atleast_1d(1, [3, 4])
    (array([1]), array([3, 4]))

    """
    if len(arys) == 1:
        result = asanyarray(arys[0])
        if result.ndim == 0:
            result = result.reshape(1)
        return result
    res = []
    for ary in arys:
        result = asanyarray(ary)
        if result.ndim == 0:
            result = result.reshape(1)
        res.append(result)
    return tuple(res)


def atleast_1d() -> list[Array]:
  ...


def atleast_1d(x: ArrayLike, /) -> Array:
  ...


def atleast_1d(x: ArrayLike, y: ArrayLike, /, *arys: ArrayLike) -> list[Array]:
  ...


def atleast_1d(*arys: ArrayLike) -> Array | list[Array]:
  """Convert inputs to arrays with at least 1 dimension.

  JAX implementation of :func:`numpy.atleast_1d`.

  Args:
    zero or more arraylike arguments.

  Returns:
    an array or list of arrays corresponding to the input values. Arrays
    of shape ``()`` are converted to shape ``(1,)``, and arrays with other
    shapes are returned unchanged.

  See also:
    - :func:`jax.numpy.asarray`
    - :func:`jax.numpy.atleast_2d`
    - :func:`jax.numpy.atleast_3d`

  Examples:
    Scalar arguments are converted to 1D, length-1 arrays:

    >>> x = jnp.float32(1.0)
    >>> jnp.atleast_1d(x)
    Array([1.], dtype=float32)

    Higher dimensional inputs are returned unchanged:

    >>> y = jnp.arange(4)
    >>> jnp.atleast_1d(y)
    Array([0, 1, 2, 3], dtype=int32)

    Multiple arguments can be passed to the function at once, in which
    case a list of results is returned:

    >>> jnp.atleast_1d(x, y)
    [Array([1.], dtype=float32), Array([0, 1, 2, 3], dtype=int32)]
  """
  util.check_arraylike("atleast_1d", *arys)
  if len(arys) == 1:
    return array(arys[0], copy=False, ndmin=1)
  else:
    return [array(arr, copy=False, ndmin=1) for arr in arys]

