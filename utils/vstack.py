
def vstack(
    tup: Sequence[ArrayLike],
    *,
    dtype: DTypeLike | None = None,
    casting: CastingModes | None = "same_kind",
):
    _concat_check(tup, dtype, out=None)
    tensors = _concat_cast_helper(tup, dtype=dtype, casting=casting)
    return torch.vstack(tensors)


def vstack(tensors: TensorSequenceType) -> TensorLikeType:
    torch._check(len(tensors) > 0, lambda: "vstack expects a non-empty TensorList")
    aligned_tensors = atleast_2d(*tensors)
    return cat(aligned_tensors, 0)


def vstack(g: jit_utils.GraphContext, tensor_list: _C.Value):
    tensor_list = atleast_2d(g, tensor_list)
    return g.op("ConcatFromSequence", tensor_list, axis_i=0, new_axis_i=0)


def vstack(blocks, format=None, dtype=None):
    """
    Stack sparse arrays vertically (row wise).

    Parameters
    ----------
    blocks : sequence of sparse matrices or arrays
        sequence of sparse arrays with compatible shapes
    format : str, optional
        sparse format of the result (e.g., "csr")
        by default an appropriate sparse array format is returned.
        This choice is subject to change.
    dtype : dtype, optional
        The data-type of the output array. If not given, the dtype is
        determined from that of `blocks`.

    Returns
    -------
    new_array : sparse matrix or array
        If any block in blocks is a sparse array, return a sparse array.
        Otherwise return a sparse matrix.

        If you want a sparse array built from blocks that are not sparse
        arrays, use ``block(vstack(blocks))`` or convert one block
        e.g. ``blocks[0] = csr_array(blocks[0])``.

    See Also
    --------
    hstack : stack sparse matrices horizontally (column wise)

    Examples
    --------
    >>> from scipy.sparse import coo_array, vstack
    >>> A = coo_array([[1, 2], [3, 4]])
    >>> B = coo_array([[5, 6]])
    >>> vstack([A, B]).toarray()
    array([[1, 2],
           [3, 4],
           [5, 6]])

    """
    blocks = np.asarray(blocks, dtype='object')
    if any(isinstance(b, sparray) for b in blocks.flat):
        return _block([[b] for b in blocks], format, dtype)
    else:
        return _block([[b] for b in blocks], format, dtype, return_spmatrix=True)


def vstack(tup, *, dtype=None, casting="same_kind"):
    """
    Stack arrays in sequence vertically (row wise).

    This is equivalent to concatenation along the first axis after 1-D arrays
    of shape `(N,)` have been reshaped to `(1,N)`. Rebuilds arrays divided by
    `vsplit`.

    This function makes most sense for arrays with up to 3 dimensions. For
    instance, for pixel-data with a height (first axis), width (second axis),
    and r/g/b channels (third axis). The functions `concatenate`, `stack` and
    `block` provide more general stacking and concatenation operations.

    Parameters
    ----------
    tup : sequence of ndarrays
        The arrays must have the same shape along all but the first axis.
        1-D arrays must have the same length. In the case of a single
        array_like input, it will be treated as a sequence of arrays; i.e.,
        each element along the zeroth axis is treated as a separate array.

    dtype : str or dtype
        If provided, the destination array will have this dtype. Cannot be
        provided together with `out`.

        .. versionadded:: 1.24

    casting : {'no', 'equiv', 'safe', 'same_kind', 'unsafe'}, optional
        Controls what kind of data casting may occur. Defaults to 'same_kind'.

        .. versionadded:: 1.24

    Returns
    -------
    stacked : ndarray
        The array formed by stacking the given arrays, will be at least 2-D.

    See Also
    --------
    concatenate : Join a sequence of arrays along an existing axis.
    stack : Join a sequence of arrays along a new axis.
    block : Assemble an nd-array from nested lists of blocks.
    hstack : Stack arrays in sequence horizontally (column wise).
    dstack : Stack arrays in sequence depth wise (along third axis).
    column_stack : Stack 1-D arrays as columns into a 2-D array.
    vsplit : Split an array into multiple sub-arrays vertically (row-wise).
    unstack : Split an array into a tuple of sub-arrays along an axis.

    Examples
    --------
    >>> import numpy as np
    >>> a = np.array([1, 2, 3])
    >>> b = np.array([4, 5, 6])
    >>> np.vstack((a,b))
    array([[1, 2, 3],
           [4, 5, 6]])

    >>> a = np.array([[1], [2], [3]])
    >>> b = np.array([[4], [5], [6]])
    >>> np.vstack((a,b))
    array([[1],
           [2],
           [3],
           [4],
           [5],
           [6]])

    """
    arrs = atleast_2d(*tup)
    if not isinstance(arrs, tuple):
        arrs = (arrs,)
    return _nx.concatenate(arrs, 0, dtype=dtype, casting=casting)


def vstack(tup: np.ndarray | Array | Sequence[ArrayLike],
           dtype: DTypeLike | None = None) -> Array:
  """Vertically stack arrays.

  JAX implementation of :func:`numpy.vstack`.

  For arrays of two or more dimensions, this is equivalent to
  :func:`jax.numpy.concatenate` with ``axis=0``.

  Args:
    tup: a sequence of arrays to stack; each must have the same shape along all
      but the first axis. If a single array is given it will be treated
      equivalently to `tup = unstack(tup)`, but the implementation will avoid
      explicit unstacking.
    dtype: optional dtype of the resulting array. If not specified, the dtype
      will be determined via type promotion rules described in :ref:`type-promotion`.

  Returns:
    the stacked result.

  See also:
    - :func:`jax.numpy.stack`: stack along arbitrary axes
    - :func:`jax.numpy.concatenate`: concatenation along existing axes.
    - :func:`jax.numpy.hstack`: stack horizontally, i.e. along axis 1.
    - :func:`jax.numpy.dstack`: stack depth-wise, i.e. along axis 2.

  Examples:
    Scalar values:

    >>> jnp.vstack([1, 2, 3])
    Array([[1],
           [2],
           [3]], dtype=int32, weak_type=True)

    1D arrays:

    >>> x = jnp.arange(4)
    >>> y = jnp.ones(4)
    >>> jnp.vstack([x, y])
    Array([[0., 1., 2., 3.],
           [1., 1., 1., 1.]], dtype=float32)

    2D arrays:

    >>> x = x.reshape(1, 4)
    >>> y = y.reshape(1, 4)
    >>> jnp.vstack([x, y])
    Array([[0., 1., 2., 3.],
           [1., 1., 1., 1.]], dtype=float32)
  """
  arrs: Array | list[Array]
  if isinstance(tup, (np.ndarray, Array)):
    arrs = api.vmap(atleast_2d)(tup)
  else:
    util.check_arraylike("vstack", *tup)
    arrs = [atleast_2d(m) for m in tup]
  return concatenate(arrs, axis=0, dtype=dtype)

