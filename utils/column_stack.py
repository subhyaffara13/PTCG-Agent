
def column_stack(
    tup: Sequence[ArrayLike],
    *,
    dtype: DTypeLike | None = None,
    casting: CastingModes | None = "same_kind",
):
    # XXX: in numpy 1.24 column_stack does not have dtype and casting keywords
    # but row_stack does. (because row_stack is an alias for vstack, really).
    # Hence add these keywords here for consistency.
    _concat_check(tup, dtype, out=None)
    tensors = _concat_cast_helper(tup, dtype=dtype, casting=casting)
    return torch.column_stack(tensors)


def column_stack(tensors: TensorSequenceType) -> TensorLikeType:
    aligned_tensors = tuple(
        x if x.ndim > 1 else x.reshape((x.numel(), 1)) for x in tensors
    )
    return cat(aligned_tensors, 1)


def column_stack(tup):
    """
    Stack 1-D arrays as columns into a 2-D array.

    Take a sequence of 1-D arrays and stack them as columns
    to make a single 2-D array. 2-D arrays are stacked as-is,
    just like with `hstack`.  1-D arrays are turned into 2-D columns
    first.

    Parameters
    ----------
    tup : sequence of 1-D or 2-D arrays.
        Arrays to stack. All of them must have the same first dimension.

    Returns
    -------
    stacked : 2-D array
        The array formed by stacking the given arrays.

    See Also
    --------
    stack, hstack, vstack, concatenate

    Examples
    --------
    >>> import numpy as np
    >>> a = np.array((1,2,3))
    >>> b = np.array((4,5,6))
    >>> np.column_stack((a,b))
    array([[1, 4],
           [2, 5],
           [3, 6]])

    """
    arrays = []
    for v in tup:
        arr = asanyarray(v)
        if arr.ndim < 2:
            arr = array(arr, copy=None, subok=True, ndmin=2).T
        arrays.append(arr)
    return _nx.concatenate(arrays, 1)


def column_stack(tup: np.ndarray | Array | Sequence[ArrayLike]) -> Array:
  """Stack arrays column-wise.

  JAX implementation of :func:`numpy.column_stack`.

  For arrays of two or more dimensions, this is equivalent to
  :func:`jax.numpy.concatenate` with ``axis=1``.

  Args:
    tup: a sequence of arrays to stack; each must have the same leading dimension.
      Input arrays will be promoted to at least rank 2. If a single array is given
      it will be treated equivalently to `tup = unstack(tup)`, but the implementation
      will avoid explicit unstacking.
    dtype: optional dtype of the resulting array. If not specified, the dtype
      will be determined via type promotion rules described in :ref:`type-promotion`.

  Returns:
    the stacked result.

  See also:
    - :func:`jax.numpy.stack`: stack along arbitrary axes
    - :func:`jax.numpy.concatenate`: concatenation along existing axes.
    - :func:`jax.numpy.vstack`: stack vertically, i.e. along axis 0.
    - :func:`jax.numpy.hstack`: stack horizontally, i.e. along axis 1.
    - :func:`jax.numpy.dstack`: stack depth-wise, i.e. along axis 2.

  Examples:
    Scalar values:

    >>> jnp.column_stack([1, 2, 3])
    Array([[1, 2, 3]], dtype=int32, weak_type=True)

    1D arrays:

    >>> x = jnp.arange(3)
    >>> y = jnp.ones(3)
    >>> jnp.column_stack([x, y])
    Array([[0., 1.],
           [1., 1.],
           [2., 1.]], dtype=float32)

    2D arrays:

    >>> x = x.reshape(3, 1)
    >>> y = y.reshape(3, 1)
    >>> jnp.column_stack([x, y])
    Array([[0., 1.],
           [1., 1.],
           [2., 1.]], dtype=float32)
  """
  arrs: Array | list[Array] | np.ndarray
  if isinstance(tup, (np.ndarray, Array)):
    arrs = api.vmap(lambda x: atleast_2d(x).T)(tup) if tup.ndim < 3 else tup
  else:
    util.check_arraylike("column_stack", *tup)
    arrs = [atleast_2d(arr).T if arr.ndim < 2 else arr for arr in map(asarray, tup)]
  return concatenate(arrs, axis=1)

