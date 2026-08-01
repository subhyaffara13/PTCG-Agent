
def squeeze(array, axis=None):
    """
    Framework-agnostic version of squeeze operation.
    """
    if is_numpy_array(array):
        return np.squeeze(array, axis=axis)
    elif is_torch_tensor(array):
        return array.squeeze() if axis is None else array.squeeze(dim=axis)
    else:
        raise ValueError(f"Type not supported for squeeze: {type(array)}.")


def squeeze(li: list[int], dim: int):
    out: list[int] = []
    wrapped_dim = maybe_wrap_dim(dim, len(li))
    for i in range(len(li)):
        if i == wrapped_dim:
            if li[i] != 1:
                out.append(li[i])
        else:
            out.append(li[i])
    return out


def squeeze(x, dim=None):
    assert isinstance(x, TensorBox)
    if dim is None:
        return TensorBox(SqueezeView.create(x.data))

    dim = (
        V.graph.sizevars.guard_int(dim)
        if isinstance(dim, (int, sympy.Expr))
        else tuple(V.graph.sizevars.guard_int(d) for d in dim)
    )
    dim = canonicalize_dims(len(x.get_size()), dim)  # type: ignore[call-overload]
    dims = OrderedSet((dim,) if not isinstance(dim, tuple) else dim)

    new_shape = []
    for d, s in enumerate(x.get_size()):
        if not (d in dims and V.graph.sizevars.guard_or_false(sympy.Eq(s, 1))):
            new_shape.append(s)

    # squeeze does nothing if the size isn't 1
    return view(x, new_shape) if new_shape != x.get_size() else x


def squeeze(a: ArrayLike, axis=None):
    if axis == ():
        result = a
    elif axis is None:
        result = a.squeeze()
    else:
        if isinstance(axis, tuple):
            result = a
            for ax in axis:
                result = a.squeeze(ax)
        else:
            result = a.squeeze(axis)
    return result


def squeeze(a: TensorLikeType, dim: DimsType | None = None) -> TensorLikeType:
    from torch.fx.experimental.symbolic_shapes import guard_or_false

    if dim is None:
        dims = tuple(idx for idx, size in enumerate(a.shape) if size == 1)
        return prims.squeeze(a, dims) if dims else prims.view_of(a)

    ndim = a.ndim

    dim = utils.canonicalize_dims(ndim, dim)
    dims = (dim,) if isinstance(dim, Dim) else dim
    # Short-circuits if the tensor has no dimensions
    if ndim == 0:
        if not (len(dims) == 0 or dims == (0,)):
            raise AssertionError(
                f"Expected dims to be empty or (0,) for 0-dim tensor, got {dims}"
            )
        return prims.view_of(a)

    # Note: squeeze does not modify tensors when the given dim is not a dimension of length 1
    # would it be better if we just not allow 1 for unbacked at runtiume?
    dims = tuple(d for d in dims if guard_or_false(a.shape[d] == 1))
    if len(dims) == 0:
        return prims.view_of(a)
    if len(dims) == 1:
        return prims.squeeze(a, dims)
    dims_list = list(dims)
    dims_list = sorted(dims_list, reverse=True)
    for i in dims_list:
        a = squeeze(a, i)
    return a


def squeeze(g: jit_utils.GraphContext, self, dim=None):
    if dim is None:
        return g.op("Squeeze", self)

    # dim as a tensor
    if not symbolic_helper._is_constant(dim):
        return symbolic_helper._squeeze_helper(g, self, [dim])

    dim = symbolic_helper._get_const(dim, "i", "dim")

    input_rank = symbolic_helper._get_tensor_rank(self)
    adjusted_dim = dim
    if input_rank is not None and dim < 0:
        adjusted_dim += input_rank
    dim_size = symbolic_helper._get_tensor_dim_size(self, adjusted_dim)
    if (dim < 0 and input_rank is None) or dim_size is None:
        # If onnx shape inference is not on, export always as dynamic.
        # Because we cannot tell if observed static shape is also static at runtime.
        # create "cond" node (condition is shape[i]==1)
        dim_constant = g.op("Constant", value_t=torch.tensor([dim]))
        size = symbolic_helper._size_helper(g, self, dim_constant)
        const_one = g.op("Constant", value_t=torch.ones(1, dtype=torch.int64))
        cond = g.op("Equal", size, const_one)
        # create the "If" node and add the "then" and "else" blocks to it.
        if_op, (if_context, else_context), _ = jit_utils.add_op_with_blocks(
            g, "If", cond, n_blocks=2
        )
        squeeze_ = symbolic_helper._squeeze_helper(if_context, self, [dim])
        utils._add_output_to_block(if_context.block, squeeze_)
        identity_ = else_context.op("Identity", self)
        utils._add_output_to_block(else_context.block, identity_)
        return if_op

    # For static input shape
    dim = adjusted_dim
    if dim_size > 1:
        warnings.warn(
            "This model contains a squeeze operation on dimension "
            + str(dim)
            + ". The size of "
            + "this dimension in the given input is "
            + str(dim_size)
            + ". The model will "
            + "be exported without the squeeze node. If the model is intended to be used with dynamic "
            + "input shapes, please export with dynamic_axes argument.",
            stacklevel=2,
        )
        return self
    return symbolic_helper._squeeze_helper(g, self, [dim])


def squeeze(g: jit_utils.GraphContext, self, dim=None):
    if dim is None:
        return g.op("Squeeze", self)

    squeeze_dim = symbolic_helper._get_const(dim, "i", "dim")
    # Handle negative dims
    if squeeze_dim < 0:
        rank = symbolic_helper._get_tensor_rank(self)
        if rank is not None:
            warnings.warn(
                "ONNX export squeeze with negative axis "
                + str(squeeze_dim)
                + " might cause the onnx model to be incorrect. "
                + "Negative axis is not supported in ONNX. "
                + "Axis is converted to "
                + str(squeeze_dim + rank)
                + " based on input shape at export time. "
                + "Passing an tensor of different rank in execution will be incorrect.",
                stacklevel=2,
            )
            squeeze_dim += rank
        else:
            return symbolic_helper._unimplemented(
                "squeeze", "negative axis with unknown input rank", self
            )

    dim_size = symbolic_helper._get_tensor_dim_size(self, squeeze_dim)
    if dim_size is None:
        warnings.warn(
            "This model contains a squeeze operation on dimension "
            + str(squeeze_dim)
            + " on an input "
            + "with unknown shape. Note that if the size of dimension "
            + str(squeeze_dim)
            + " of the input "
            + "is not 1, the ONNX model will return an error. Opset version 11 supports squeezing on "
            + "non-singleton dimensions, it is recommended to export this model using opset "
            + "version 11 or higher.",
            stacklevel=2,
        )
        return symbolic_helper._squeeze_helper(g, self, axes_i=[squeeze_dim])
    if dim_size > 1:
        warnings.warn(
            "This model contains a squeeze operation on dimension "
            + str(squeeze_dim)
            + ". The size of "
            + "this dimension in the given input is "
            + str(dim_size)
            + ". The model will "
            + "be exported without the squeeze node. If the model is intended to be used with dynamic "
            + "input shapes, please use opset version 11 to "
            + "export the model.",
            stacklevel=2,
        )
        return self

    warnings.warn(
        "This model contains a squeeze operation on dimension "
        + str(squeeze_dim)
        + ". If the model is "
        + "intended to be used with dynamic input shapes, please use opset version 11 to export the model.",
        stacklevel=2,
    )
    return symbolic_helper._squeeze_helper(g, self, axes_i=[squeeze_dim])


def squeeze(x: Array, /, axis: int | tuple[int, ...]) -> Array:
    if isinstance(axis, int):
        axis = (axis,)
    for a in axis:
        if x.shape[a] != 1:
            raise ValueError("squeezed dimensions must be equal to 1")
    axes = _normalize_axes(axis, x.ndim)
    # Remove this once pytorch 1.14 is released with the above PR #89017.
    sequence = [a - i for i, a in enumerate(axes)]
    for a in sequence:
        x = torch.squeeze(x, a)
    return x


def squeeze(a, axis=None):
    """
    Remove axes of length one from `a`.

    Parameters
    ----------
    a : array_like
        Input data.
    axis : None or int or tuple of ints, optional
        Selects a subset of the entries of length one in the
        shape. If an axis is selected with shape entry greater than
        one, an error is raised.

    Returns
    -------
    squeezed : ndarray
        The input array, but with all or a subset of the
        dimensions of length 1 removed. This is always `a` itself
        or a view into `a`. Note that if all axes are squeezed,
        the result is a 0d array and not a scalar.

    Raises
    ------
    ValueError
        If `axis` is not None, and an axis being squeezed is not of length 1

    See Also
    --------
    expand_dims : The inverse operation, adding entries of length one
    reshape : Insert, remove, and combine dimensions, and resize existing ones

    Examples
    --------
    >>> import numpy as np
    >>> x = np.array([[[0], [1], [2]]])
    >>> x.shape
    (1, 3, 1)
    >>> np.squeeze(x).shape
    (3,)
    >>> np.squeeze(x, axis=0).shape
    (3, 1)
    >>> np.squeeze(x, axis=1).shape
    Traceback (most recent call last):
    ...
    ValueError: cannot select an axis to squeeze out which has size
    not equal to one
    >>> np.squeeze(x, axis=2).shape
    (1, 3)
    >>> x = np.array([[1234]])
    >>> x.shape
    (1, 1)
    >>> np.squeeze(x)
    array(1234)  # 0d array
    >>> np.squeeze(x).shape
    ()
    >>> np.squeeze(x)[()]
    1234

    """
    try:
        squeeze = a.squeeze
    except AttributeError:
        return _wrapit(a, 'squeeze', axis=axis)
    if axis is None:
        return squeeze()
    else:
        return squeeze(axis=axis)


def squeeze(array: ArrayLike, dimensions: Sequence[int]) -> Array:
  """Squeeze any number of size 1 dimensions from an array."""
  ndim = np.ndim(array)
  dimensions = tuple(sorted(canonicalize_axis(i, ndim) for i in dimensions))
  if not dimensions and isinstance(array, Array):
    return array
  return squeeze_p.bind(array, dimensions=dimensions)


def squeeze(a: ArrayLike, axis: int | Sequence[int] | None = None) -> Array:
  """Remove one or more length-1 axes from array

  JAX implementation of :func:`numpy.sqeeze`, implemented via :func:`jax.lax.squeeze`.

  Args:
    a: input array
    axis: integer or sequence of integers specifying axes to remove. If any specified
      axis does not have a length of 1, an error is raised. If not specified, squeeze
      all length-1 axes in ``a``.

  Returns:
    copy of ``a`` with length-1 axes removed.

  Notes:
    Unlike :func:`numpy.squeeze`, :func:`jax.numpy.squeeze` will return a copy rather
    than a view of the input array. However, under JIT, the compiler will optimize-away
    such copies when possible, so this doesn't have performance impacts in practice.

  See Also:
    - :func:`jax.numpy.expand_dims`: the inverse of ``squeeze``: add dimensions of length 1.
    - :meth:`jax.Array.squeeze`: equivalent functionality via an array method.
    - :func:`jax.lax.squeeze`: equivalent XLA API.
    - :func:`jax.numpy.ravel`: flatten an array into a 1D shape.
    - :func:`jax.numpy.reshape`: general array reshape.

  Examples:
    >>> x = jnp.array([[[0]], [[1]], [[2]]])
    >>> x.shape
    (3, 1, 1)

    Squeeze all length-1 dimensions:

    >>> jnp.squeeze(x)
    Array([0, 1, 2], dtype=int32)
    >>> _.shape
    (3,)

    Equivalent while specifying the axes explicitly:

    >>> jnp.squeeze(x, axis=(1, 2))
    Array([0, 1, 2], dtype=int32)

    Attempting to squeeze a non-unit axis results in an error:

    >>> jnp.squeeze(x, axis=0)  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
      ...
    ValueError: cannot select an axis to squeeze out which has size not equal to one, got shape=(3, 1, 1) and dimensions=(0,)

    For convenience, this functionality is also available via the
    :meth:`jax.Array.squeeze` method:

    >>> x.squeeze()
    Array([0, 1, 2], dtype=int32)
  """
  arr = util.ensure_arraylike("squeeze", a)
  return _squeeze(arr, _ensure_index_tuple(axis) if axis is not None else None)

