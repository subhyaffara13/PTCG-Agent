
def argmin(
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
    mask_input = _combine_input_and_mask(argmin, input, mask)
    if mask_input.layout == torch.strided:
        return torch.argmin(mask_input, dim, bool(keepdim)).to(dtype=dtype)
    else:
        raise ValueError(
            f"masked argmin expects strided tensor (got {mask_input.layout} tensor)"
        )


def argmin(
    a: ArrayLike,
    axis: AxisLike = None,
    out: OutArray | None = None,
    *,
    keepdims: KeepDims = False,
):
    if a.is_complex():
        raise NotImplementedError(f"argmin with dtype={a.dtype}.")

    axis = _util.allow_only_single_axis(axis)

    if a.dtype == torch.bool:
        # RuntimeError: "argmin_cpu" not implemented for 'Bool'
        a = a.to(torch.uint8)

    return torch.argmin(a, axis)


def argmin(
    g: jit_utils.GraphContext,
    input: torch._C.Value,
    dim: torch._C.Value,
    keepdim: bool,
):
    return symbolic_helper._argmin_argmax_helper(g, input, dim, keepdim, "ArgMin")


def argmin(
    g: jit_utils.GraphContext,
    input: torch._C.Value,
    dim: torch._C.Value,
    keepdim: bool,
):
    return symbolic_helper._argmin_argmax_helper(g, input, dim, keepdim, "ArgMin")


def argmin(iterable, *, key=None):
    """
    Index of the first occurrence of a minimum value in an iterable.

        >>> argmin('efghabcdijkl')
        4
        >>> argmin([3, 2, 1, 0, 4, 2, 1, 0])
        3

    For example, look up a label corresponding to the position
    of a value that minimizes a cost function::

        >>> def cost(x):
        ...     "Days for a wound to heal given a subject's age."
        ...     return x**2 - 20*x + 150
        ...
        >>> labels =  ['homer', 'marge', 'bart', 'lisa', 'maggie']
        >>> ages =    [  35,      30,      10,      9,      1    ]

        # Fastest healing family member
        >>> labels[argmin(ages, key=cost)]
        'bart'

        # Age with fastest healing
        >>> min(ages, key=cost)
        10

    """
    if key is not None:
        iterable = map(key, iterable)
    return min(enumerate(iterable), key=itemgetter(1))[0]


def argmin(a, axis=None, out=None, *, keepdims=np._NoValue):
    """
    Returns the indices of the minimum values along an axis.

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
        Array of indices into the array. It has the same shape as `a.shape`
        with the dimension along `axis` removed. If `keepdims` is set to True,
        then the size of `axis` will be 1 with the resulting array having same
        shape as `a.shape`.

    See Also
    --------
    ndarray.argmin, argmax
    amin : The minimum value along a given axis.
    unravel_index : Convert a flat index into an index tuple.
    take_along_axis : Apply ``np.expand_dims(index_array, axis)``
                      from argmin to an array as if by calling min.

    Notes
    -----
    In case of multiple occurrences of the minimum values, the indices
    corresponding to the first occurrence are returned.

    Examples
    --------
    >>> import numpy as np
    >>> a = np.arange(6).reshape(2,3) + 10
    >>> a
    array([[10, 11, 12],
           [13, 14, 15]])
    >>> np.argmin(a)
    0
    >>> np.argmin(a, axis=0)
    array([0, 0, 0])
    >>> np.argmin(a, axis=1)
    array([0, 0])

    Indices of the minimum elements of an N-dimensional array:

    >>> a.flat[np.argmin(a)]
    10
    >>> ind = np.unravel_index(np.argmin(a, axis=None), a.shape)
    >>> ind
    (0, 0)
    >>> a[ind]
    10

    >>> b = np.arange(6) + 10
    >>> b[4] = 10
    >>> b
    array([10, 11, 12, 13, 10, 15])
    >>> np.argmin(b)  # Only the first occurrence is returned.
    0

    >>> x = np.array([[4,2,3], [1,0,3]])
    >>> index_array = np.argmin(x, axis=-1)
    >>> # Same as np.amin(x, axis=-1, keepdims=True)
    >>> np.take_along_axis(x, np.expand_dims(index_array, axis=-1), axis=-1)
    array([[2],
           [0]])
    >>> # Same as np.amax(x, axis=-1)
    >>> np.take_along_axis(x, np.expand_dims(index_array, axis=-1),
    ...     axis=-1).squeeze(axis=-1)
    array([2, 0])

    Setting `keepdims` to `True`,

    >>> x = np.arange(24).reshape((2, 3, 4))
    >>> res = np.argmin(x, axis=1, keepdims=True)
    >>> res.shape
    (2, 1, 4)
    """
    kwds = {'keepdims': keepdims} if keepdims is not np._NoValue else {}
    return _wrapfunc(a, 'argmin', axis=axis, out=out, **kwds)


def argmin(operand: ArrayLike, axis: int,
           index_dtype: DTypeLike) -> Array:
  """Computes the index of the minimum element along ``axis``."""
  index_dtype = dtypes.check_and_canonicalize_user_dtype(index_dtype, 'argmin')
  return argmin_p.bind(operand, axes=(axis,), index_dtype=index_dtype)


def argmin(a: ArrayLike, axis: int | None = None, out: None = None,
           keepdims: bool | None = None) -> Array:
  """Return the index of the minimum value of an array.

  JAX implementation of :func:`numpy.argmin`.

  Args:
    a: input array
    axis: optional integer specifying the axis along which to find the minimum
      value. If ``axis`` is not specified, ``a`` will be flattened.
    out: unused by JAX
    keepdims: if True, then return an array with the same number of dimensions
      as ``a``.

  Returns:
    an array containing the index of the minimum value along the specified axis.

  Note:
    When the minimum value occurs more than once along a particular axis, the
    smallest index is returned.

  See also:
    - :func:`jax.numpy.argmax`: return the index of the maximum value.
    - :func:`jax.numpy.nanargmin`: compute ``argmin`` while ignoring NaN values.

  Examples:
    >>> x = jnp.array([1, 3, 5, 4, 2])
    >>> jnp.argmin(x)
    Array(0, dtype=int32)

    >>> x = jnp.array([[1, 3, 2],
    ...                [5, 4, 1]])
    >>> jnp.argmin(x, axis=1)
    Array([0, 2], dtype=int32)

    >>> jnp.argmin(x, axis=1, keepdims=True)
    Array([[0],
           [2]], dtype=int32)
  """
  arr = util.ensure_arraylike("argmin", a)
  if out is not None:
    raise NotImplementedError("The 'out' argument to jnp.argmin is not supported.")
  return _argmin(arr, None if axis is None else operator.index(axis),
                 keepdims=bool(keepdims))

