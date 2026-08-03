import math


def vector_norm(
    x: TensorLikeType,
    ord: float | int = 2,
    dim: DimsType | None = None,
    keepdim: bool = False,
    *,
    dtype: torch.dtype | None = None,
) -> Tensor:
    from torch.fx.experimental.symbolic_shapes import guard_or_false

    check_fp_or_complex(x.dtype, "linalg.vector_norm")

    if isinstance(dim, Dim):
        dim = [dim]  # type: ignore[assignment]

    _check_vector_norm_args(x, ord, dim)

    _check_norm_dtype(dtype, x.dtype, "linalg.vector_norm")

    computation_dtype, result_dtype = utils.reduction_dtypes(
        x, utils.REDUCTION_OUTPUT_TYPE_KIND.COMPLEX_TO_FLOAT, dtype
    )

    to_result_dtype = partial(_maybe_convert_to_dtype, dtype=result_dtype)

    # Implementation
    if ord == 0.0:
        return torch.sum(torch.ne(x, 0.0), dim=dim, keepdim=keepdim, dtype=result_dtype)
    elif ord == float("inf"):
        return to_result_dtype(torch.amax(torch.abs(x), dim=dim, keepdim=keepdim))  # type: ignore[return-value,arg-type]
    elif ord == float("-inf"):
        return to_result_dtype(torch.amin(torch.abs(x), dim=dim, keepdim=keepdim))  # type: ignore[return-value,arg-type]
    else:
        # From here on the computation dtype is important as the reduction is non-trivial
        x = _maybe_convert_to_dtype(x, computation_dtype)  # type: ignore[assignment]
        reduce_sum = partial(torch.sum, dim=dim, keepdim=keepdim)

        is_ord_even = ord % 2 == 0 if isinstance(ord, IntLike) else ord % 2.0 == 0.0
        if dim == []:
            dim = None

        if (dim is None and guard_or_false(x.numel() == 1)) or (
            dim is not None
            and (x.ndim > 0 and all(guard_or_false(x.shape[d] == 1) for d in dim))
        ):
            if x.ndim > 64:
                raise RuntimeError(
                    f"Received a tensor with {x.ndim} dimensions, but only tensors with up to 64 dims are supported!"
                )
            x = torch.abs(x)
            if keepdim or x.ndim == 0:
                return to_result_dtype(x).contiguous()
            elif dim is None:
                return to_result_dtype(x).flatten()[0]
            else:
                new_shape = [s for d, s in enumerate(x.shape) if d not in dim]
                return to_result_dtype(x.view(new_shape)).contiguous()

        if not (is_ord_even and utils.is_float_dtype(x.dtype)):
            x = torch.abs(x)
        return to_result_dtype(torch.pow(reduce_sum(torch.pow(x, ord)), 1.0 / ord))  # type: ignore[return-value]


def vector_norm(
    x: Array,
    /,
    xp: Namespace,
    *,
    axis: int | tuple[int, ...] | None = None,
    keepdims: bool = False,
    ord: JustInt | JustFloat = 2,
) -> Array:
    # xp.linalg.norm tries to do a matrix norm whenever axis is a 2-tuple or
    # when axis=None and the input is 2-D, so to force a vector norm, we make
    # it so the input is 1-D (for axis=None), or reshape so that norm is done
    # on a single dimension.
    if axis is None:
        # Note: xp.linalg.norm() doesn't handle 0-D arrays
        _x = x.ravel()
        _axis = 0
    elif isinstance(axis, tuple):
        # Note: The axis argument supports any number of axes, whereas
        # xp.linalg.norm() only supports a single axis for vector norm.
        normalized_axis = cast(
            "tuple[int, ...]",
            normalize_axis_tuple(axis, x.ndim),  # pyright: ignore[reportCallIssue]
        )
        rest = tuple(i for i in range(x.ndim) if i not in normalized_axis)
        newshape = axis + rest
        _x = xp.transpose(x, newshape).reshape(
            (math.prod([x.shape[i] for i in axis]), *[x.shape[i] for i in rest]))
        _axis = 0
    else:
        _x = x
        _axis = axis

    res = xp.linalg.norm(_x, axis=_axis, ord=ord)

    if keepdims:
        # We can't reuse xp.linalg.norm(keepdims) because of the reshape hacks
        # above to avoid matrix norm logic.
        shape = list(x.shape)
        axes = cast(
            "tuple[int, ...]",
            normalize_axis_tuple(  # pyright: ignore[reportCallIssue]
                range(x.ndim) if axis is None else axis,
                x.ndim,
            ),
        )
        for i in axes:
            shape[i] = 1
        res = xp.reshape(res, tuple(shape))

    return res


def vector_norm(
    x: Array,
    /,
    *,
    axis: int | tuple[int, ...] | None = None,
    keepdims: bool = False,
    # JustFloat stands for inf | -inf, which are not valid for Literal
    ord: JustInt | JustFloat = 2,
    **kwargs: object,
) -> Array:
    # torch.vector_norm incorrectly treats axis=() the same as axis=None
    if axis == ():
        out = kwargs.get('out')
        if out is None:
            dtype = None
            if x.dtype == torch.complex64:
                dtype = torch.float32
            elif x.dtype == torch.complex128:
                dtype = torch.float64

            out = torch.zeros_like(x, dtype=dtype)

        # The norm of a single scalar works out to abs(x) in every case except
        # for ord=0, which is x != 0.
        if ord == 0:
            out[:] = (x != 0)
        else:
            out[:] = torch.abs(x)
        return out
    return torch.linalg.vector_norm(x, ord=ord, axis=axis, keepdim=keepdims, **kwargs)


def vector_norm(x, /, *, axis=None, keepdims=False, ord=2):
    """
    Computes the vector norm of a vector (or batch of vectors) ``x``.

    This function is Array API compatible.

    Parameters
    ----------
    x : array_like
        Input array.
    axis : {None, int, 2-tuple of ints}, optional
        If an integer, ``axis`` specifies the axis (dimension) along which
        to compute vector norms. If an n-tuple, ``axis`` specifies the axes
        (dimensions) along which to compute batched vector norms. If ``None``,
        the vector norm must be computed over all array values (i.e.,
        equivalent to computing the vector norm of a flattened array).
        Default: ``None``.
    keepdims : bool, optional
        If this is set to True, the axes which are normed over are left in
        the result as dimensions with size one. Default: False.
    ord : {int, float, inf, -inf}, optional
        The order of the norm. For details see the table under ``Notes``
        in `numpy.linalg.norm`.

    See Also
    --------
    numpy.linalg.norm : Generic norm function

    Examples
    --------
    >>> from numpy import linalg as LA
    >>> a = np.arange(9) + 1
    >>> a
    array([1, 2, 3, 4, 5, 6, 7, 8, 9])
    >>> b = a.reshape((3, 3))
    >>> b
    array([[1, 2, 3],
           [4, 5, 6],
           [7, 8, 9]])

    >>> LA.vector_norm(b)
    16.881943016134134
    >>> LA.vector_norm(b, ord=np.inf)
    9.0
    >>> LA.vector_norm(b, ord=-np.inf)
    1.0

    >>> LA.vector_norm(b, ord=0)
    9.0
    >>> LA.vector_norm(b, ord=1)
    45.0
    >>> LA.vector_norm(b, ord=-1)
    0.3534857623790153
    >>> LA.vector_norm(b, ord=2)
    16.881943016134134
    >>> LA.vector_norm(b, ord=-2)
    0.8058837395885292

    """
    x = asanyarray(x)
    shape = list(x.shape)
    if axis is None:
        # Note: np.linalg.norm() doesn't handle 0-D arrays
        x = x.ravel()
        _axis = 0
    elif isinstance(axis, tuple):
        # Note: The axis argument supports any number of axes, whereas
        # np.linalg.norm() only supports a single axis for vector norm.
        normalized_axis = normalize_axis_tuple(axis, x.ndim)
        rest = tuple(i for i in range(x.ndim) if i not in normalized_axis)
        newshape = axis + rest
        x = _core_transpose(x, newshape).reshape(
            (
                prod([x.shape[i] for i in axis], dtype=int),
                *[x.shape[i] for i in rest]
            )
        )
        _axis = 0
    else:
        _axis = axis

    res = norm(x, axis=_axis, ord=ord)

    if keepdims:
        # We can't reuse np.linalg.norm(keepdims) because of the reshape hacks
        # above to avoid matrix norm logic.
        _axis = normalize_axis_tuple(
            range(len(shape)) if axis is None else axis, len(shape)
        )
        for i in _axis:
            shape[i] = 1
        res = res.reshape(tuple(shape))

    return res


def vector_norm(x: ArrayLike, /, *, axis: int | tuple[int, ...] | None = None, keepdims: bool = False,
                ord: int | str = 2) -> Array:
  """Compute the vector norm of a vector or batch of vectors.

  JAX implementation of :func:`numpy.linalg.vector_norm`.

  Args:
    x: N-dimensional array for which to take the norm.
    axis: optional axis along which to compute the vector norm. If None (default)
      then ``x`` is flattened and the norm is taken over all values.
    keepdims: if True, keep the reduced dimensions in the output.
    ord: A string or int specifying the type of norm; default is the 2-norm.
      See :func:`numpy.linalg.norm` for details on available options.

  Returns:
    array containing the norm of ``x``.

  See also:
    - :func:`jax.numpy.linalg.matrix_norm`: Norm of a matrix or stack of matrices.
    - :func:`jax.numpy.linalg.norm`: More general matrix or vector norm.

  Examples:
    Norm of a single vector:

    >>> x = jnp.array([1., 2., 3.])
    >>> jnp.linalg.vector_norm(x)
    Array(3.7416575, dtype=float32)

    Norm of a batch of vectors:

    >>> x = jnp.array([[1., 2., 3.],
    ...                [4., 5., 7.]])
    >>> jnp.linalg.vector_norm(x, axis=1)
    Array([3.7416575, 9.486833 ], dtype=float32)
  """
  x = ensure_arraylike('jnp.linalg.vector_norm', x)
  if ord is None or ord == 2:
    return ufuncs.sqrt(reductions.sum(ufuncs.real(x * ufuncs.conj(x)), axis=axis,
                                      keepdims=keepdims))
  elif ord == np.inf:
    return reductions.amax(ufuncs.abs(x), axis=axis, keepdims=keepdims, initial=0)
  elif ord == -np.inf:
    return reductions.amin(ufuncs.abs(x), axis=axis, keepdims=keepdims)
  elif ord == 0:
    return reductions.sum(x != 0, dtype=jnp.finfo(lax.dtype(x)).dtype,
                          axis=axis, keepdims=keepdims)
  elif ord == 1:
    # Numpy has a special case for ord == 1 as an optimization. We don't
    # really need the optimization (XLA could do it for us), but the Numpy
    # code has slightly different type promotion semantics, so we need a
    # special case too.
    return reductions.sum(ufuncs.abs(x), axis=axis, keepdims=keepdims)
  elif isinstance(ord, str):
    msg = f"Invalid order '{ord}' for vector norm."
    if ord == "inf":
      msg += "Use 'jax.numpy.inf' instead."
    if ord == "-inf":
      msg += "Use '-jax.numpy.inf' instead."
    raise ValueError(msg)
  else:
    abs_x = ufuncs.abs(x)
    ord_arr = lax._const(abs_x, ord)
    ord_inv = lax._const(abs_x, 1. / ord_arr)
    out = reductions.sum(abs_x ** ord_arr, axis=axis, keepdims=keepdims)
    return ufuncs.power(out, ord_inv)

