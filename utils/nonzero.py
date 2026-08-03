import sys
import math


def nonzero(self):
    torch._check_not_implemented(
        exp_config.meta_nonzero_assume_all_nonzero,
        lambda: "The register_meta function for torch.nonzero() raises unimplemented by default, "
        "as a correct data-independent implementation does not exist. This implementation "
        "returns a fake value, assuming all elements of the tensor are non-zero. "
        "To enable this registration, please set "
        "'torch.fx.experimental._config.meta_nonzero_assume_all_nonzero' to True.",
    )
    return torch.empty_strided(
        (self.numel(), self.dim()),
        (1, self.numel()),
        dtype=torch.long,
        device=self.device,
    )


def nonzero(a: ArrayLike):
    return torch.nonzero(a, as_tuple=True)


def nonzero(fake_mode: FakeTensorMode, func: OpOverload, arg: FakeTensor) -> FakeTensor:
    if (
        fake_mode.shape_env is None
        or not fake_mode.shape_env.allow_dynamic_output_shape_ops
    ):
        # Without symints/symfloats, cannot handle this
        raise DynamicOutputShapeException(func)

    if (nnz := arg.nonzero_memo) is None:
        # Avoid importing sympy at a module level
        from torch.fx.experimental.symbolic_shapes import (
            _constrain_range_for_size,
            has_free_symbols,
        )
        from torch.utils._sympy.numbers import IntInfinity
        from torch.utils._sympy.value_ranges import bound_sympy

        if not has_free_symbols(arg.numel()) and arg.numel() == 0:
            # If numel is zero, then the output size must be zero.
            # In this case, we must not allocate an unbacked SymInt,
            # because if we do, it will immediately get refined to
            # zero, but this will be inconsistent with size oblivious
            # tests (which will continue to claim that the unbacked
            # symint cannot equal zero).  We could also unconditionally
            # allocate an unbacked SymInt and not refine its range,
            # but this seems more precise.
            nnz = 0
        else:
            nnz = fake_mode.shape_env.create_unbacked_symint()

            maxval = sys.maxsize - 1

            if not has_free_symbols(arg.numel()):
                maxval = int(arg.numel())
            else:
                prod_node = math.prod(arg.shape).node  # type: ignore[union-attr]
                prod_range = bound_sympy(
                    prod_node.expr, prod_node.shape_env.var_to_range
                )
                if isinstance(prod_range.upper, IntInfinity):
                    maxval = sys.maxsize - 1
                else:
                    maxval = prod_range.upper

            _constrain_range_for_size(nnz, max=maxval)

        arg.nonzero_memo = nnz  # pyrefly: ignore[bad-assignment]
    return arg.new_empty_strided((nnz, arg.dim()), (1, nnz), dtype=torch.int64)  # type: ignore[return]


def nonzero(g: jit_utils.GraphContext, input):
    """Emitted from `torch.nonzero(x, as_tuple=False)`"""
    return t(g, g.op("NonZero", input))


def nonzero(x: Array, /, xp: Namespace, **kwargs: object) -> tuple[Array, ...]:
    if x.ndim == 0:
        raise ValueError("nonzero() does not support zero-dimensional arrays")
    return xp.nonzero(x, **kwargs)


def nonzero(x: Array, /, **kwargs: object) -> tuple[Array, ...]:
    if x.ndim == 0:
        raise ValueError("nonzero() does not support zero-dimensional arrays")
    return torch.nonzero(x, as_tuple=True, **kwargs)


def nonzero(a):
    """
    Return the indices of the elements that are non-zero.

    Returns a tuple of arrays, one for each dimension of `a`,
    containing the indices of the non-zero elements in that
    dimension. The values in `a` are always tested and returned in
    row-major, C-style order.

    To group the indices by element, rather than dimension, use `argwhere`,
    which returns a row for each non-zero element.

    Parameters
    ----------
    a : array_like
        Input array.

    Returns
    -------
    tuple_of_arrays : tuple
        Indices of elements that are non-zero.

    See Also
    --------
    flatnonzero :
        Return indices that are non-zero in the flattened version of the input
        array.
    ndarray.nonzero :
        Equivalent ndarray method.
    count_nonzero :
        Counts the number of non-zero elements in the input array.

    Notes
    -----
    While the nonzero values can be obtained with ``a[nonzero(a)]``, it is
    recommended to use ``x[x.astype(np.bool)]`` or ``x[x != 0]`` instead, which
    will correctly handle 0-d arrays.

    Examples
    --------
    >>> import numpy as np
    >>> x = np.array([[3, 0, 0], [0, 4, 0], [5, 6, 0]])
    >>> x
    array([[3, 0, 0],
           [0, 4, 0],
           [5, 6, 0]])
    >>> np.nonzero(x)
    (array([0, 1, 2, 2]), array([0, 1, 0, 1]))

    >>> x[np.nonzero(x)]
    array([3, 4, 5, 6])
    >>> np.transpose(np.nonzero(x))
    array([[0, 0],
           [1, 1],
           [2, 0],
           [2, 1]])

    A common use for ``nonzero`` is to find the indices of an array, where
    a condition is True.  Given an array `a`, the condition `a` > 3 is a
    boolean array and since False is interpreted as 0, np.nonzero(a > 3)
    yields the indices of the `a` where the condition is true.

    >>> a = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    >>> a > 3
    array([[False, False, False],
           [ True,  True,  True],
           [ True,  True,  True]])
    >>> np.nonzero(a > 3)
    (array([1, 1, 1, 2, 2, 2]), array([0, 1, 2, 0, 1, 2]))

    Using this result to index `a` is equivalent to using the mask directly:

    >>> a[np.nonzero(a > 3)]
    array([4, 5, 6, 7, 8, 9])
    >>> a[a > 3]  # prefer this spelling
    array([4, 5, 6, 7, 8, 9])

    ``nonzero`` can also be called as a method of the array.

    >>> (a > 3).nonzero()
    (array([1, 1, 1, 2, 2, 2]), array([0, 1, 2, 0, 1, 2]))

    """
    return _wrapfunc(a, 'nonzero')


def nonzero(
    a: ArrayLike,
    /,
    *,
    size: int,
    axes: tuple[int, ...] | None = None,
    dtype: DTypeLike = 'int32',
) -> tuple[Array, ...]:
  """Return indices of nonzero elements.

  This is a batch-aware implementation of :func:`numpy.nonzero` built on a
  HiJAX primitive.

  Args:
    a: N-dimensional array.
    size: static integer specifying the number of nonzero entries to return.
    axes: optional tuple of integers specifying the axes to compute the result over.
      Defaults to None (all axes).
    dtype: optional datatype for the returned indices. Defaults to int32.

  Returns:
    Tuple of length ``len(axes)`` containing the indices of each nonzero value.
  """
  a, = core.auto_insert_reshard(a)
  out_dtype = dtypes._maybe_canonicalize_explicit_dtype(np.dtype(dtype), "nonzero")
  axes = util.canonicalize_axis_tuple(axes, np.ndim(a))
  prim = Nonzero(
    core.typeof(a),
    size=size,
    axes=axes,
    out_dtype=out_dtype,
  )
  return prim(a)


def nonzero(a: ArrayLike, *, size: int | None = None,
            fill_value: None | ArrayLike | tuple[ArrayLike, ...] = None
    ) -> tuple[Array, ...]:
  """Return indices of nonzero elements of an array.

  JAX implementation of :func:`numpy.nonzero`.

  Because the size of the output of ``nonzero`` is data-dependent, the function
  is not compatible with JIT and other transformations. The JAX version adds
  the optional ``size`` argument which must be specified statically for
  ``jnp.nonzero`` to be used within JAX's transformations.

  Args:
    a: N-dimensional array.
    size: optional static integer specifying the number of nonzero entries to
      return. If there are more nonzero elements than the specified ``size``,
      then indices will be truncated at the end. If there are fewer nonzero
      elements than the specified size, then indices will be padded with
      ``fill_value``, which defaults to zero.
    fill_value: optional padding value when ``size`` is specified. Defaults to 0.

  Returns:
    Tuple of JAX Arrays of length ``a.ndim``, containing the indices of each
    nonzero value.

  See also:
    - :func:`jax.numpy.flatnonzero`
    - :func:`jax.numpy.where`

  Examples:

    One-dimensional array returns a length-1 tuple of indices:

    >>> x = jnp.array([0, 5, 0, 6, 0, 7])
    >>> jnp.nonzero(x)
    (Array([1, 3, 5], dtype=int32),)

    Two-dimensional array returns a length-2 tuple of indices:

    >>> x = jnp.array([[0, 5, 0],
    ...                [6, 0, 7]])
    >>> jnp.nonzero(x)
    (Array([0, 1, 1], dtype=int32), Array([1, 0, 2], dtype=int32))

    In either case, the resulting tuple of indices can be used directly to extract
    the nonzero values:

    >>> indices = jnp.nonzero(x)
    >>> x[indices]
    Array([5, 6, 7], dtype=int32)

    The output of ``nonzero`` has a dynamic shape, because the number of returned
    indices depends on the contents of the input array. As such, it is incompatible
    with JIT and other JAX transformations:

    >>> x = jnp.array([0, 5, 0, 6, 0, 7])
    >>> jax.jit(jnp.nonzero)(x)  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
      ...
    ConcretizationTypeError: Abstract tracer value encountered where concrete value is expected: traced array with shape int32[].
    The size argument of jnp.nonzero must be statically specified to use jnp.nonzero within JAX transformations.

    This can be addressed by passing a static ``size`` parameter to specify the
    desired output shape:

    >>> nonzero_jit = jax.jit(jnp.nonzero, static_argnames='size')
    >>> nonzero_jit(x, size=3)
    (Array([1, 3, 5], dtype=int32),)

    If ``size`` does not match the true size, the result will be either truncated or padded:

    >>> nonzero_jit(x, size=2)  # size < 3: indices are truncated
    (Array([1, 3], dtype=int32),)
    >>> nonzero_jit(x, size=5)  # size > 3: indices are padded with zeros.
    (Array([1, 3, 5, 0, 0], dtype=int32),)

    You can specify a custom fill value for the padding using the ``fill_value`` argument:

    >>> nonzero_jit(x, size=5, fill_value=len(x))
    (Array([1, 3, 5, 6, 6], dtype=int32),)
  """
  arr = util.ensure_arraylike("nonzero", a)
  del a
  if np.ndim(arr) == 0:
    raise ValueError("Calling nonzero on 0d arrays is not allowed. "
                     "Use jnp.atleast_1d(scalar).nonzero() instead.")
  mask = arr if arr.dtype == bool else (arr != 0)
  calculated_size_ = mask.sum() if size is None else size
  calculated_size: int = core.concrete_dim_or_error(calculated_size_,
    "The size argument of jnp.nonzero must be statically specified "
    "to use jnp.nonzero within JAX transformations.")
  if arr.size == 0 or calculated_size == 0:
    return tuple(array_creation.zeros(calculated_size, int) for dim in arr.shape)
  flat_indices = reductions.cumsum(
      bincount(reductions.cumsum(mask), length=calculated_size))
  strides: np.ndarray = np.cumprod(arr.shape[::-1])[::-1] // arr.shape
  if all(core.is_constant_dim(d) for d in strides):
    strides = strides.astype(flat_indices.dtype)
  out = tuple((flat_indices // stride) % size for stride, size in zip(strides, arr.shape))
  if fill_value is not None:
    fill_value_tup = fill_value if isinstance(fill_value, tuple) else arr.ndim * (fill_value,)
    if any(np.shape(val) != () for val in fill_value_tup):
      raise ValueError(f"fill_value must be a scalar or a tuple of length {arr.ndim}; got {fill_value}")
    fill_mask = arange(calculated_size) >= mask.sum()
    out = tuple(where(fill_mask, fval, entry) for fval, entry in safe_zip(fill_value_tup, out))
  return out

