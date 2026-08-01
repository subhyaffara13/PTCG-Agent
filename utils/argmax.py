
def argmax(
    self: list[int], dim: Optional[int] = None, keepdim: bool = False
) -> list[int]:
    if dim is None:
        return []
    return _reduce_along_dim(self, dim, keepdim)


def argmax(
    input: Tensor | MaskedTensor,
    dim: int | None = None,
    *,
    keepdim: bool | None = False,
    dtype: DType | None = None,
    mask: Tensor | None = None,
) -> Tensor:
    """\
{reduction_signature}
{reduction_descr}
{reduction_identity_dtype}
{reduction_args}
{reduction_example}"""
    if dtype is None:
        dtype = input.dtype
    mask_input = _combine_input_and_mask(argmax, input, mask)
    if mask_input.layout == torch.strided:
        return torch.argmax(mask_input, dim, bool(keepdim)).to(dtype=dtype)
    else:
        raise ValueError(
            f"masked argmax expects strided tensor (got {mask_input.layout} tensor)"
        )


def argmax(seq, key=lambda x: x, start=0, end=None):
    seq = seq[start:end]
    if len(seq) == 0:
        return None
    return seq.index(max(seq, key=key)) + start


def argmax(
    a: ArrayLike,
    axis: AxisLike = None,
    out: OutArray | None = None,
    *,
    keepdims: KeepDims = False,
):
    if a.is_complex():
        raise NotImplementedError(f"argmax with dtype={a.dtype}.")

    axis = _util.allow_only_single_axis(axis)

    if a.dtype == torch.bool:
        # RuntimeError: "argmax_cpu" not implemented for 'Bool'
        a = a.to(torch.uint8)

    return torch.argmax(a, axis)


def argmax(
    g: jit_utils.GraphContext,
    input: torch._C.Value,
    dim: torch._C.Value,
    keepdim: bool,
):
    return symbolic_helper._argmin_argmax_helper(g, input, dim, keepdim, "ArgMax")


def argmax(
    g: jit_utils.GraphContext,
    input: torch._C.Value,
    dim: torch._C.Value,
    keepdim: bool,
):
    return symbolic_helper._argmin_argmax_helper(g, input, dim, keepdim, "ArgMax")


def argmax(iterable, *, key=None):
    """
    Index of the first occurrence of a maximum value in an iterable.

        >>> argmax('abcdefghabcd')
        7
        >>> argmax([0, 1, 2, 3, 3, 2, 1, 0])
        3

    For example, identify the best machine learning model::

        >>> models =   ['svm', 'random forest', 'knn', 'naïve bayes']
        >>> accuracy = [  68,        61,          84,       72      ]

        # Most accurate model
        >>> models[argmax(accuracy)]
        'knn'

        # Best accuracy
        >>> max(accuracy)
        84

    """
    if key is not None:
        iterable = map(key, iterable)
    return max(enumerate(iterable), key=itemgetter(1))[0]


def argmax(random, z):
  """Returns argmax of flattened z with ties split randomly.

  Args:
    random: Random number generator, e.g., np.random.RandomState()
    z: np.array
  Returns:
    integer representing index of argmax
  """
  inds = np.arange(z.size)
  random.shuffle(inds)
  z_shuffled = z[inds]
  ind_max = np.argmax(z_shuffled)
  return inds[ind_max]


def argmax(a, axis=None, out=None, *, keepdims=np._NoValue):
    """
    Returns the indices of the maximum values along an axis.

    Parameters
    ----------
    a : array_like
        Input array.
    axis : int, optional
        By default, the index is into the flattened array, otherwise
        along the specified axis.
    out : array, optional
        If provided, the result will be inserted into this array. It should
        be of the appropriate shape and dtype.
    keepdims : bool, optional
        If this is set to True, the axes which are reduced are left
        in the result as dimensions with size one. With this option,
        the result will broadcast correctly against the array.

        .. versionadded:: 1.22.0

    Returns
    -------
    index_array : ndarray of ints
        Array of indices into the array. It has the same shape as ``a.shape``
        with the dimension along `axis` removed. If `keepdims` is set to True,
        then the size of `axis` will be 1 with the resulting array having same
        shape as ``a.shape``.

    See Also
    --------
    ndarray.argmax, argmin
    amax : The maximum value along a given axis.
    unravel_index : Convert a flat index into an index tuple.
    take_along_axis : Apply ``np.expand_dims(index_array, axis)``
                      from argmax to an array as if by calling max.

    Notes
    -----
    In case of multiple occurrences of the maximum values, the indices
    corresponding to the first occurrence are returned.

    Examples
    --------
    >>> import numpy as np
    >>> a = np.arange(6).reshape(2,3) + 10
    >>> a
    array([[10, 11, 12],
           [13, 14, 15]])
    >>> np.argmax(a)
    5
    >>> np.argmax(a, axis=0)
    array([1, 1, 1])
    >>> np.argmax(a, axis=1)
    array([2, 2])

    Indexes of the maximal elements of an N-dimensional array:

    >>> a.flat[np.argmax(a)]
    15
    >>> ind = np.unravel_index(np.argmax(a, axis=None), a.shape)
    >>> ind
    (1, 2)
    >>> a[ind]
    15

    >>> b = np.arange(6)
    >>> b[1] = 5
    >>> b
    array([0, 5, 2, 3, 4, 5])
    >>> np.argmax(b)  # Only the first occurrence is returned.
    1

    >>> x = np.array([[4,2,3], [1,0,3]])
    >>> index_array = np.argmax(x, axis=-1)
    >>> # Same as np.amax(x, axis=-1, keepdims=True)
    >>> np.take_along_axis(x, np.expand_dims(index_array, axis=-1), axis=-1)
    array([[4],
           [3]])
    >>> # Same as np.amax(x, axis=-1)
    >>> np.take_along_axis(x, np.expand_dims(index_array, axis=-1),
    ...     axis=-1).squeeze(axis=-1)
    array([4, 3])

    Setting `keepdims` to `True`,

    >>> x = np.arange(24).reshape((2, 3, 4))
    >>> res = np.argmax(x, axis=1, keepdims=True)
    >>> res.shape
    (2, 1, 4)
    """
    kwds = {'keepdims': keepdims} if keepdims is not np._NoValue else {}
    return _wrapfunc(a, 'argmax', axis=axis, out=out, **kwds)


def argmax(operand: ArrayLike, axis: int,
           index_dtype: DTypeLike) -> Array:
  """Computes the index of the maximum element along ``axis``."""
  index_dtype = dtypes.check_and_canonicalize_user_dtype(index_dtype, 'argmax')
  return argmax_p.bind(operand, axes=(axis,), index_dtype=index_dtype)


def argmax(a: ArrayLike, axis: int | None = None, out: None = None,
           keepdims: bool | None = None) -> Array:
  """Return the index of the maximum value of an array.

  JAX implementation of :func:`numpy.argmax`.

  Args:
    a: input array
    axis: optional integer specifying the axis along which to find the maximum
      value. If ``axis`` is not specified, ``a`` will be flattened.
    out: unused by JAX
    keepdims: if True, then return an array with the same number of dimensions
      as ``a``.

  Returns:
    an array containing the index of the maximum value along the specified axis.

  See also:
    - :func:`jax.numpy.argmin`: return the index of the minimum value.
    - :func:`jax.numpy.nanargmax`: compute ``argmax`` while ignoring NaN values.

  Note:
    When the maximum value occurs more than once along a particular axis, the
    smallest index is returned.

  Examples:
    >>> x = jnp.array([1, 3, 5, 4, 2])
    >>> jnp.argmax(x)
    Array(2, dtype=int32)

    >>> x = jnp.array([[1, 3, 2],
    ...                [5, 4, 1]])
    >>> jnp.argmax(x, axis=1)
    Array([1, 0], dtype=int32)

    >>> jnp.argmax(x, axis=1, keepdims=True)
    Array([[1],
           [0]], dtype=int32)
  """
  arr = util.ensure_arraylike("argmax", a)
  if out is not None:
    raise NotImplementedError("The 'out' argument to jnp.argmax is not supported.")
  return _argmax(arr, None if axis is None else operator.index(axis),
                 keepdims=bool(keepdims))

