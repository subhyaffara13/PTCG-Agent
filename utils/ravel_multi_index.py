import math


def ravel_multi_index(multi_index, dims, mode="raise", order="C"):
    """
    ravel_multi_index(multi_index, dims, mode='raise', order='C')

    Converts a tuple of index arrays into an array of flat
    indices, applying boundary modes to the multi-index.

    Parameters
    ----------
    multi_index : tuple of array_like
        A tuple of integer arrays, one array for each dimension.
    dims : tuple of ints
        The shape of array into which the indices from ``multi_index`` apply.
    mode : {'raise', 'wrap', 'clip'}, optional
        Specifies how out-of-bounds indices are handled.  Can specify
        either one mode or a tuple of modes, one mode per index.

        * 'raise' -- raise an error (default)
        * 'wrap' -- wrap around
        * 'clip' -- clip to the range

        In 'clip' mode, a negative index which would normally
        wrap will clip to 0 instead.
    order : {'C', 'F'}, optional
        Determines whether the multi-index should be viewed as
        indexing in row-major (C-style) or column-major
        (Fortran-style) order.

    Returns
    -------
    raveled_indices : ndarray
        An array of indices into the flattened version of an array
        of dimensions ``dims``.

    See Also
    --------
    unravel_index

    Examples
    --------
    >>> import numpy as np
    >>> arr = np.array([[3,6,6],[4,5,1]])
    >>> np.ravel_multi_index(arr, (7,6))
    array([22, 41, 37])
    >>> np.ravel_multi_index(arr, (7,6), order='F')
    array([31, 41, 13])
    >>> np.ravel_multi_index(arr, (4,6), mode='clip')
    array([22, 23, 19])
    >>> np.ravel_multi_index(arr, (4,4), mode=('clip','wrap'))
    array([12, 13, 13])

    >>> np.ravel_multi_index((3,1,4,1), (6,7,8,9))
    1621
    """
    return multi_index


def ravel_multi_index(multi_index: Sequence[ArrayLike], dims: Sequence[int],
                      mode: str = 'raise', order: str = 'C',
                      *, dtype: DTypeLike | None = None) -> Array:
  """Convert multi-dimensional indices into flat indices.

  JAX implementation of :func:`numpy.ravel_multi_index`

  Args:
    multi_index: sequence of integer arrays containing indices in each dimension.
    dims: sequence of integer sizes; must have ``len(dims) == len(multi_index)``
    mode: how to handle out-of bound indices. Options are

      - ``"raise"`` (default): raise a ValueError. This mode is incompatible
        with :func:`~jax.jit` or other JAX transformations.
      - ``"clip"``: clip out-of-bound indices to valid range.
      - ``"wrap"``: wrap out-of-bound indices to valid range.
      - ``"ignore"``: do not coerce or check input indices. Behavior is
        undefined if indices are out of bounds.

    order: ``"C"`` (default) or ``"F"``, specify whether to assume C-style
      row-major order or Fortran-style column-major order.
    dtype: the desired output dtype. If not specified, the dtype is determined
      by standard type promotion rules of the input multi_index.

  Returns:
    array of flattened indices

  See also:
    :func:`jax.numpy.unravel_index`: inverse of this function.

  Examples:
    Define a 2-dimensional array and a sequence of indices of even values:

    >>> x = jnp.array([[2., 3., 4.],
    ...                [5., 6., 7.]])
    >>> indices = jnp.where(x % 2 == 0)
    >>> indices
    (Array([0, 0, 1], dtype=int32), Array([0, 2, 1], dtype=int32))
    >>> x[indices]
    Array([2., 4., 6.], dtype=float32)

    Compute the flattened indices:

    >>> indices_flat = jnp.ravel_multi_index(indices, x.shape)
    >>> indices_flat
    Array([0, 2, 4], dtype=int32)

    These flattened indices can be used to extract the same values from the
    flattened ``x`` array:

    >>> x_flat = x.ravel()
    >>> x_flat
    Array([2., 3., 4., 5., 6., 7.], dtype=float32)
    >>> x_flat[indices_flat]
    Array([2., 4., 6.], dtype=float32)

    The original indices can be recovered with :func:`~jax.numpy.unravel_index`:

    >>> jnp.unravel_index(indices_flat, x.shape)
    (Array([0, 0, 1], dtype=int32), Array([0, 2, 1], dtype=int32))
  """
  assert len(multi_index) == len(dims), f"len(multi_index)={len(multi_index)} != len(dims)={len(dims)}"
  dims = tuple(core.concrete_or_error(operator.index, d, "in `dims` argument of ravel_multi_index().") for d in dims)
  multi_index_arr = list(util.ensure_arraylike_tuple("ravel_multi_index", multi_index))

  if dtype is None:
    dtype = dtypes.result_type(int, *multi_index_arr)
  else:
    dtype = dtypes.check_and_canonicalize_user_dtype(dtype, "ravel_multi_index")
  if not issubdtype(dtype, np.integer):
    raise ValueError(f"{dtype=} is not an integer type.")
  if math.prod(dims) - 1 > iinfo(dtype).max:
    raise ValueError(
      f"jnp.ravel_multi_index: {dtype=} not large enough to hold flattened"
      f" index for {dims=}. Use the dtype argument to pass a suitable"
      " dtype (e.g. dtype=np.min_scalar_type(prod(dims))).")

  for index in multi_index_arr:
    if mode == 'raise':
      core.concrete_or_error(array, index,
        "The error occurred because ravel_multi_index was jit-compiled"
        " with mode='raise'. Use mode='wrap' or mode='clip' instead.")
    if not issubdtype(_dtype(index), np.integer):
      raise TypeError("only int indices permitted")
  if mode == "raise":
    if any(reductions.any((i < 0) | (i >= d)) for i, d in zip(multi_index_arr, dims)):
      raise ValueError("invalid entry in coordinates array")
  elif mode == "clip":
    multi_index_arr = [clip(i, 0, d - 1) for i, d in zip(multi_index_arr, dims)]
  elif mode == "wrap":
    multi_index_arr = [i % d for i, d in zip(multi_index_arr, dims)]
  elif mode == "ignore":
    pass
  else:
    raise ValueError(f"invalid mode={mode!r}. Expected 'raise', 'wrap', 'clip', or 'ignore'.")

  if order == "F":
    strides = np.cumprod((1,) + dims[:-1])
  elif order == "C":
    strides = np.cumprod((1,) + dims[1:][::-1])[::-1]
  else:
    raise ValueError(f"invalid order={order!r}. Expected 'C' or 'F'")

  result = array(0, dtype=dtype)
  for i, s in zip(multi_index_arr, strides):
    result = result + i.astype(dtype) * int(s)
  return result


def ravel_multi_index(idx, sizes):
    val = 0
    mult = 1
    for i, s in zip(idx[::-1], sizes[::-1]):
        val += i * mult
        mult *= s
    return val

