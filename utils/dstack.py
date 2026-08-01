
def dstack(
    tup: Sequence[ArrayLike],
    *,
    dtype: DTypeLike | None = None,
    casting: CastingModes | None = "same_kind",
):
    # XXX: in numpy 1.24 dstack does not have dtype and casting keywords
    # but {h,v}stack do.  Hence add them here for consistency.
    _concat_check(tup, dtype, out=None)
    tensors = _concat_cast_helper(tup, dtype=dtype, casting=casting)
    return torch.dstack(tensors)


def dstack(tensors: TensorSequenceType) -> TensorLikeType:
    torch._check(len(tensors) > 0, lambda: "dstack expects a non-empty TensorList")
    aligned_tensors = atleast_3d(*tensors)
    return cat(aligned_tensors, 2)


def dstack(tup):
    """
    Stack arrays in sequence depth wise (along third axis).

    This is equivalent to concatenation along the third axis after 2-D arrays
    of shape `(M,N)` have been reshaped to `(M,N,1)` and 1-D arrays of shape
    `(N,)` have been reshaped to `(1,N,1)`. Rebuilds arrays divided by
    `dsplit`.

    This function makes most sense for arrays with up to 3 dimensions. For
    instance, for pixel-data with a height (first axis), width (second axis),
    and r/g/b channels (third axis). The functions `concatenate`, `stack` and
    `block` provide more general stacking and concatenation operations.

    Parameters
    ----------
    tup : sequence of arrays
        The arrays must have the same shape along all but the third axis.
        1-D or 2-D arrays must have the same shape.

    Returns
    -------
    stacked : ndarray
        The array formed by stacking the given arrays, will be at least 3-D.

    See Also
    --------
    concatenate : Join a sequence of arrays along an existing axis.
    stack : Join a sequence of arrays along a new axis.
    block : Assemble an nd-array from nested lists of blocks.
    vstack : Stack arrays in sequence vertically (row wise).
    hstack : Stack arrays in sequence horizontally (column wise).
    column_stack : Stack 1-D arrays as columns into a 2-D array.
    dsplit : Split array along third axis.

    Examples
    --------
    >>> import numpy as np
    >>> a = np.array((1,2,3))
    >>> b = np.array((4,5,6))
    >>> np.dstack((a,b))
    array([[[1, 4],
            [2, 5],
            [3, 6]]])

    >>> a = np.array([[1],[2],[3]])
    >>> b = np.array([[4],[5],[6]])
    >>> np.dstack((a,b))
    array([[[1, 4]],
           [[2, 5]],
           [[3, 6]]])

    """
    arrs = atleast_3d(*tup)
    if not isinstance(arrs, tuple):
        arrs = (arrs,)
    return _nx.concatenate(arrs, 2)


def dstack(tup: np.ndarray | Array | Sequence[ArrayLike],
           dtype: DTypeLike | None = None) -> Array:
  """Stack arrays depth-wise.

  JAX implementation of :func:`numpy.dstack`.

  For arrays of three or more dimensions, this is equivalent to
  :func:`jax.numpy.concatenate` with ``axis=2``.

  Args:
    tup: a sequence of arrays to stack; each must have the same shape along all
      but the third axis. Input arrays will be promoted to at least rank 3. If a
      single array is given it will be treated equivalently to `tup = unstack(tup)`,
      but the implementation will avoid explicit unstacking.
    dtype: optional dtype of the resulting array. If not specified, the dtype
      will be determined via type promotion rules described in :ref:`type-promotion`.

  Returns:
    the stacked result.

  See also:
    - :func:`jax.numpy.stack`: stack along arbitrary axes
    - :func:`jax.numpy.concatenate`: concatenation along existing axes.
    - :func:`jax.numpy.vstack`: stack vertically, i.e. along axis 0.
    - :func:`jax.numpy.hstack`: stack horizontally, i.e. along axis 1.

  Examples:
    Scalar values:

    >>> jnp.dstack([1, 2, 3])
    Array([[[1, 2, 3]]], dtype=int32, weak_type=True)

    1D arrays:

    >>> x = jnp.arange(3)
    >>> y = jnp.ones(3)
    >>> jnp.dstack([x, y])
    Array([[[0., 1.],
            [1., 1.],
            [2., 1.]]], dtype=float32)

    2D arrays:

    >>> x = x.reshape(1, 3)
    >>> y = y.reshape(1, 3)
    >>> jnp.dstack([x, y])
    Array([[[0., 1.],
            [1., 1.],
            [2., 1.]]], dtype=float32)
  """
  arrs: Array | list[Array]
  if isinstance(tup, (np.ndarray, Array)):
    arrs = api.vmap(atleast_3d)(tup)
  else:
    util.check_arraylike("dstack", *tup)
    tup = util.ensure_arraylike_tuple("dstack", tup)
    arrs = [atleast_3d(m) for m in tup]
  return concatenate(arrs, axis=2, dtype=dtype)

