
def atleast_3d(*tensors):
    r"""
    Returns a 3-dimensional view of each input tensor with zero dimensions.
    Input tensors with three or more dimensions are returned as-is.

    Args:
        input (Tensor or sequence of Tensors): tensor(s) to be converted to at least 3-dimensional.

    Returns:
        output (Tensor or tuple of Tensors)

    Example:

        >>> x = torch.tensor(0.5)
        >>> x
        tensor(0.5000)
        >>> torch.atleast_3d(x)
        tensor([[[0.5000]]])
        >>> y = torch.arange(4).view(2, 2)
        >>> y
        tensor([[0, 1],
                [2, 3]])
        >>> torch.atleast_3d(y)
        tensor([[[0],
                 [1]],
                <BLANKLINE>
                [[2],
                 [3]]])
        >>> x = torch.tensor(1).view(1, 1, 1)
        >>> x
        tensor([[[1]]])
        >>> torch.atleast_3d(x)
        tensor([[[1]]])
        >>> x = torch.tensor(0.5)
        >>> y = torch.tensor(1.0)
        >>> torch.atleast_3d((x, y))
        (tensor([[[0.5000]]]), tensor([[[1.]]]))
        >>> torch.atleast_3d()
        ()
    """
    # This wrapper exists to support variadic args.
    if has_torch_function(tensors):
        return handle_torch_function(atleast_3d, tensors, *tensors)
    if len(tensors) == 1:
        tensors = tensors[0]
    return _VF.atleast_3d(tensors)  # type: ignore[attr-defined]


def atleast_3d(*arys: ArrayLike):
    res = torch.atleast_3d(*arys)
    if isinstance(res, tuple):
        return list(res)
    else:
        return res


def atleast_3d(
    arg: TensorLikeType | Sequence[TensorLikeType], *args: TensorLikeType
) -> TensorLikeType | tuple[TensorLikeType, ...]:
    """Reference implementation of :func:`torch.atleast_3d`."""
    if not args and isinstance(arg, collections.abc.Sequence):
        args_ = arg
    else:
        if isinstance(arg, collections.abc.Sequence):
            raise AssertionError("arg should not be a Sequence when args is provided")
        args_ = (arg,) + args
    unsqueeze_atleast_2d = partial(_unsqueeze_atleast, atleast_2d, -1)
    res = tuple(a if a.ndim >= 3 else unsqueeze_atleast_2d(a) for a in args_)
    return res if len(res) > 1 else res[0]


def atleast_3d(g: jit_utils.GraphContext, self: torch._C.Value):
    # NOTE: If it's 0D, reshape to 3D
    #       If it's 1D, unsqueeze to 3D
    #       If it's 2D, unsqueeze to 3D

    # NOTE: self could be a packed list or a tensor
    if symbolic_helper._is_value(self) and symbolic_helper._is_packed_list(self):
        tensor_list = symbolic_helper._unpack_list(self)
        new_tensor_list = []
        for tensor in tensor_list:
            new_tensor = tensor
            tensor_rank = symbolic_helper._get_tensor_rank(tensor)
            if tensor_rank == 0:
                new_tensor = symbolic_helper._reshape_helper(
                    g, new_tensor, g.op("Constant", value_t=torch.tensor([1, 1, 1]))
                )
            elif tensor_rank == 1:
                new_tensor = symbolic_helper._unsqueeze_helper(
                    g, new_tensor, axes_i=[0]
                )
                new_tensor = symbolic_helper._unsqueeze_helper(
                    g, new_tensor, axes_i=[-1]
                )
            elif tensor_rank == 2:
                new_tensor = symbolic_helper._unsqueeze_helper(
                    g, new_tensor, axes_i=[-1]
                )
            new_tensor_list.append(new_tensor)
        return g.op("SequenceConstruct", *new_tensor_list)

    tensor_rank = symbolic_helper._get_tensor_rank(self)
    if tensor_rank == 0:
        self = symbolic_helper._reshape_helper(
            g, self, g.op("Constant", value_t=torch.tensor([1, 1, 1]))
        )
    elif tensor_rank == 1:
        self = symbolic_helper._unsqueeze_helper(g, self, axes_i=[0])
        self = symbolic_helper._unsqueeze_helper(g, self, axes_i=[-1])
    elif tensor_rank == 2:
        self = symbolic_helper._unsqueeze_helper(g, self, axes_i=[-1])
    return self


def atleast_3d(*arys):
    """
    View inputs as arrays with at least three dimensions.

    Parameters
    ----------
    arys1, arys2, ... : array_like
        One or more array-like sequences.  Non-array inputs are converted to
        arrays.  Arrays that already have three or more dimensions are
        preserved.

    Returns
    -------
    res1, res2, ... : ndarray
        An array, or tuple of arrays, each with ``a.ndim >= 3``.  Copies are
        avoided where possible, and views with three or more dimensions are
        returned.  For example, a 1-D array of shape ``(N,)`` becomes a view
        of shape ``(1, N, 1)``, and a 2-D array of shape ``(M, N)`` becomes a
        view of shape ``(M, N, 1)``.

    See Also
    --------
    atleast_1d, atleast_2d

    Examples
    --------
    >>> import numpy as np
    >>> np.atleast_3d(3.0)
    array([[[3.]]])

    >>> x = np.arange(3.0)
    >>> np.atleast_3d(x).shape
    (1, 3, 1)

    >>> x = np.arange(12.0).reshape(4,3)
    >>> np.atleast_3d(x).shape
    (4, 3, 1)
    >>> np.atleast_3d(x).base is x.base  # x is a reshape, so not base itself
    True

    >>> for arr in np.atleast_3d([1, 2], [[1, 2]], [[[1, 2]]]):
    ...     print(arr, arr.shape) # doctest: +SKIP
    ...
    [[[1]
      [2]]] (1, 2, 1)
    [[[1]
      [2]]] (1, 2, 1)
    [[[1 2]]] (1, 1, 2)

    """
    res = []
    for ary in arys:
        ary = asanyarray(ary)
        if ary.ndim == 0:
            result = ary.reshape(1, 1, 1)
        elif ary.ndim == 1:
            result = ary[_nx.newaxis, :, _nx.newaxis]
        elif ary.ndim == 2:
            result = ary[:, :, _nx.newaxis]
        else:
            result = ary
        res.append(result)
    if len(res) == 1:
        return res[0]
    else:
        return tuple(res)


def atleast_3d() -> list[Array]:
  ...


def atleast_3d(x: ArrayLike, /) -> Array:
  ...


def atleast_3d(x: ArrayLike, y: ArrayLike, /, *arys: ArrayLike) -> list[Array]:
  ...


def atleast_3d(*arys: ArrayLike) -> Array | list[Array]:
  """Convert inputs to arrays with at least 3 dimensions.

  JAX implementation of :func:`numpy.atleast_3d`.

  Args:
    zero or more arraylike arguments.

  Returns:
    an array or list of arrays corresponding to the input values. Arrays
    of shape ``()`` are converted to shape ``(1, 1, 1)``, 1D arrays of
    shape ``(N,)`` are converted to shape ``(1, N, 1)``, 2D arrays of
    shape ``(M, N)`` are converted to shape ``(M, N, 1)``, and arrays
    of all other shapes are returned unchanged.

  See also:
    - :func:`jax.numpy.asarray`
    - :func:`jax.numpy.atleast_1d`
    - :func:`jax.numpy.atleast_2d`

  Examples:
    Scalar arguments are converted to 3D, size-1 arrays:

    >>> x = jnp.float32(1.0)
    >>> jnp.atleast_3d(x)
    Array([[[1.]]], dtype=float32)

    1D arrays have a unit dimension prepended and appended:

    >>> y = jnp.arange(4)
    >>> jnp.atleast_3d(y).shape
    (1, 4, 1)

    2D arrays have a unit dimension appended:

    >>> z = jnp.ones((2, 3))
    >>> jnp.atleast_3d(z).shape
    (2, 3, 1)

    Multiple arguments can be passed to the function at once, in which
    case a list of results is returned:

    >>> x3, y3 = jnp.atleast_3d(x, y)
    >>> print(x3)
    [[[1.]]]
    >>> print(y3)
    [[[0]
      [1]
      [2]
      [3]]]
  """
  util.check_arraylike("atleast_3d", *arys)
  if len(arys) == 1:
    arr = asarray(arys[0])
    if arr.ndim == 0:
      arr = lax.expand_dims(arr, dimensions=(0, 1, 2))
    elif arr.ndim == 1:
      arr = lax.expand_dims(arr, dimensions=(0, 2))
    elif arr.ndim == 2:
      arr = lax.expand_dims(arr, dimensions=(2,))
    return arr
  else:
    return [atleast_3d(arr) for arr in arys]

