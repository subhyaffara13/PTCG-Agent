
def hstack(
    tup: Sequence[ArrayLike],
    *,
    dtype: DTypeLike | None = None,
    casting: CastingModes | None = "same_kind",
):
    _concat_check(tup, dtype, out=None)
    tensors = _concat_cast_helper(tup, dtype=dtype, casting=casting)
    return torch.hstack(tensors)


def hstack(tensors: TensorSequenceType) -> TensorLikeType:
    torch._check(len(tensors) > 0, lambda: "hstack expects a non-empty TensorList")
    aligned_tensors = atleast_1d(*tensors)
    if aligned_tensors[0].ndim == 1:
        return cat(aligned_tensors, 0)
    return cat(aligned_tensors, 1)


def hstack(g: jit_utils.GraphContext, tensor_list: _C.Value):
    tensor_list = atleast_1d(g, tensor_list)
    first_tensor = g.op(
        "SequenceAt",
        tensor_list,
        g.op("Constant", value_t=torch.tensor(0, dtype=torch.long)),
    )
    first_tensor_shape = g.op("Shape", first_tensor)
    first_tensor_dim = g.op("Size", first_tensor_shape)

    const_one = g.op("Constant", value_t=torch.tensor(1, dtype=torch.long))
    equal_to_one = g.op("Equal", first_tensor_dim, const_one)

    (
        if_op_greater,
        (if_context_equal, else_context_equal),
        _,
    ) = jit_utils.add_op_with_blocks(g, "If", equal_to_one, n_blocks=2, outputs=1)
    result_if = if_context_equal.op(
        "ConcatFromSequence", tensor_list, axis_i=0, new_axis_i=0
    )
    utils._add_output_to_block(if_context_equal.block, result_if)
    result_else = else_context_equal.op(
        "ConcatFromSequence", tensor_list, axis_i=1, new_axis_i=0
    )
    utils._add_output_to_block(else_context_equal.block, result_else)
    result = if_op_greater.node().output()

    return result


def hstack(blocks, format=None, dtype=None):
    """
    Stack sparse matrices horizontally (column wise).

    Parameters
    ----------
    blocks : sequence of sparse matrices or arrays
        sequence of sparse matrices with compatible shapes
    format : str
        sparse format of the result (e.g., "csr")
        by default an appropriate sparse matrix format is returned.
        This choice is subject to change.
    dtype : dtype, optional
        The data-type of the output matrix. If not given, the dtype is
        determined from that of `blocks`.

    Returns
    -------
    new_array : sparse matrix or array
        If any block in blocks is a sparse array, return a sparse array.
        Otherwise return a sparse matrix.

        If you want a sparse array built from blocks that are not sparse
        arrays, use ``block(hstack(blocks))`` or convert one block
        e.g. ``blocks[0] = csr_array(blocks[0])``.

    See Also
    --------
    vstack : stack sparse matrices vertically (row wise)

    Examples
    --------
    >>> from scipy.sparse import coo_matrix, hstack
    >>> A = coo_matrix([[1, 2], [3, 4]])
    >>> B = coo_matrix([[5], [6]])
    >>> hstack([A,B]).toarray()
    array([[1, 2, 5],
           [3, 4, 6]])

    """
    blocks = np.asarray(blocks, dtype='object')
    if any(isinstance(b, sparray) for b in blocks.flat):
        return _block([blocks], format, dtype)
    else:
        return _block([blocks], format, dtype, return_spmatrix=True)


def hstack(tup, *, dtype=None, casting="same_kind"):
    """
    Stack arrays in sequence horizontally (column wise).

    This is equivalent to concatenation along the second axis, except for 1-D
    arrays where it concatenates along the first axis. Rebuilds arrays divided
    by `hsplit`.

    This function makes most sense for arrays with up to 3 dimensions. For
    instance, for pixel-data with a height (first axis), width (second axis),
    and r/g/b channels (third axis). The functions `concatenate`, `stack` and
    `block` provide more general stacking and concatenation operations.

    Parameters
    ----------
    tup : sequence of ndarrays
        The arrays must have the same shape along all but the second axis,
        except 1-D arrays which can be any length. In the case of a single
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
        The array formed by stacking the given arrays.

    See Also
    --------
    concatenate : Join a sequence of arrays along an existing axis.
    stack : Join a sequence of arrays along a new axis.
    block : Assemble an nd-array from nested lists of blocks.
    vstack : Stack arrays in sequence vertically (row wise).
    dstack : Stack arrays in sequence depth wise (along third axis).
    column_stack : Stack 1-D arrays as columns into a 2-D array.
    hsplit : Split an array into multiple sub-arrays
             horizontally (column-wise).
    unstack : Split an array into a tuple of sub-arrays along an axis.

    Examples
    --------
    >>> import numpy as np
    >>> a = np.array((1,2,3))
    >>> b = np.array((4,5,6))
    >>> np.hstack((a,b))
    array([1, 2, 3, 4, 5, 6])
    >>> a = np.array([[1],[2],[3]])
    >>> b = np.array([[4],[5],[6]])
    >>> np.hstack((a,b))
    array([[1, 4],
           [2, 5],
           [3, 6]])

    """
    arrs = atleast_1d(*tup)
    if not isinstance(arrs, tuple):
        arrs = (arrs,)
    # As a special case, dimension 0 of 1-dimensional arrays is "horizontal"
    if arrs and arrs[0].ndim == 1:
        return _nx.concatenate(arrs, 0, dtype=dtype, casting=casting)
    else:
        return _nx.concatenate(arrs, 1, dtype=dtype, casting=casting)


def hstack(tup: np.ndarray | Array | Sequence[ArrayLike],
           dtype: DTypeLike | None = None) -> Array:
  """Horizontally stack arrays.

  JAX implementation of :func:`numpy.hstack`.

  For arrays of one or more dimensions, this is equivalent to
  :func:`jax.numpy.concatenate` with ``axis=1``.

  Args:
    tup: a sequence of arrays to stack; each must have the same shape along all
      but the second axis. Input arrays will be promoted to at least rank 1.
      If a single array is given it will be treated equivalently to
      `tup = unstack(tup)`, but the implementation will avoid explicit unstacking.
    dtype: optional dtype of the resulting array. If not specified, the dtype
      will be determined via type promotion rules described in :ref:`type-promotion`.

  Returns:
    the stacked result.

  See also:
    - :func:`jax.numpy.stack`: stack along arbitrary axes
    - :func:`jax.numpy.concatenate`: concatenation along existing axes.
    - :func:`jax.numpy.vstack`: stack vertically, i.e. along axis 0.
    - :func:`jax.numpy.dstack`: stack depth-wise, i.e. along axis 2.

  Examples:
    Scalar values:

    >>> jnp.hstack([1, 2, 3])
    Array([1, 2, 3], dtype=int32, weak_type=True)

    1D arrays:

    >>> x = jnp.arange(3)
    >>> y = jnp.ones(3)
    >>> jnp.hstack([x, y])
    Array([0., 1., 2., 1., 1., 1.], dtype=float32)

    2D arrays:

    >>> x = x.reshape(3, 1)
    >>> y = y.reshape(3, 1)
    >>> jnp.hstack([x, y])
    Array([[0., 1.],
           [1., 1.],
           [2., 1.]], dtype=float32)
  """
  arrs: Array | list[Array]
  if isinstance(tup, (np.ndarray, Array)):
    arrs = api.vmap(atleast_1d)(tup)
    arr0_ndim = arrs.ndim - 1  # pyrefly: ignore[missing-attribute]
  else:
    util.check_arraylike("hstack", *tup)
    arrs = [atleast_1d(m) for m in tup]
    arr0_ndim = arrs[0].ndim
  return concatenate(arrs, axis=0 if arr0_ndim == 1 else 1, dtype=dtype)

