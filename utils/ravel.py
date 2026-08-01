
def ravel(a: ArrayLike, order: NotImplementedType = "C"):
    return torch.flatten(a)


def ravel(a: TensorLikeType) -> TensorLikeType:
    return reshape(a, (-1,))


def ravel(a, order='C'):
    """Return a contiguous flattened array.

    A 1-D array, containing the elements of the input, is returned.  A copy is
    made only if needed.

    As of NumPy 1.10, the returned array will have the same type as the input
    array. (for example, a masked array will be returned for a masked array
    input)

    Parameters
    ----------
    a : array_like
        Input array.  The elements in `a` are read in the order specified by
        `order`, and packed as a 1-D array.
    order : {'C','F', 'A', 'K'}, optional

        The elements of `a` are read using this index order. 'C' means
        to index the elements in row-major, C-style order,
        with the last axis index changing fastest, back to the first
        axis index changing slowest.  'F' means to index the elements
        in column-major, Fortran-style order, with the
        first index changing fastest, and the last index changing
        slowest. Note that the 'C' and 'F' options take no account of
        the memory layout of the underlying array, and only refer to
        the order of axis indexing.  'A' means to read the elements in
        Fortran-like index order if `a` is Fortran *contiguous* in
        memory, C-like order otherwise.  'K' means to read the
        elements in the order they occur in memory, except for
        reversing the data when strides are negative.  By default, 'C'
        index order is used.

    Returns
    -------
    y : array_like
        y is a contiguous 1-D array of the same subtype as `a`,
        with shape ``(a.size,)``.
        Note that matrices are special cased for backward compatibility,
        if `a` is a matrix, then y is a 1-D ndarray.

    See Also
    --------
    ndarray.flat : 1-D iterator over an array.
    ndarray.flatten : 1-D array copy of the elements of an array
                      in row-major order.
    ndarray.reshape : Change the shape of an array without changing its data.

    Notes
    -----
    In row-major, C-style order, in two dimensions, the row index
    varies the slowest, and the column index the quickest.  This can
    be generalized to multiple dimensions, where row-major order
    implies that the index along the first axis varies slowest, and
    the index along the last quickest.  The opposite holds for
    column-major, Fortran-style index ordering.

    When a view is desired in as many cases as possible, ``arr.reshape(-1)``
    may be preferable. However, ``ravel`` supports ``K`` in the optional
    ``order`` argument while ``reshape`` does not.

    Examples
    --------
    It is equivalent to ``reshape(-1, order=order)``.

    >>> import numpy as np
    >>> x = np.array([[1, 2, 3], [4, 5, 6]])
    >>> np.ravel(x)
    array([1, 2, 3, 4, 5, 6])

    >>> x.reshape(-1)
    array([1, 2, 3, 4, 5, 6])

    >>> np.ravel(x, order='F')
    array([1, 4, 2, 5, 3, 6])

    When ``order`` is 'A', it will preserve the array's 'C' or 'F' ordering:

    >>> np.ravel(x.T)
    array([1, 4, 2, 5, 3, 6])
    >>> np.ravel(x.T, order='A')
    array([1, 2, 3, 4, 5, 6])

    When ``order`` is 'K', it will preserve orderings that are neither 'C'
    nor 'F', but won't reverse axes:

    >>> a = np.arange(3)[::-1]; a
    array([2, 1, 0])
    >>> a.ravel(order='C')
    array([2, 1, 0])
    >>> a.ravel(order='K')
    array([2, 1, 0])

    >>> a = np.arange(12).reshape(2,3,2).swapaxes(1,2); a
    array([[[ 0,  2,  4],
            [ 1,  3,  5]],
           [[ 6,  8, 10],
            [ 7,  9, 11]]])
    >>> a.ravel(order='C')
    array([ 0,  2,  4,  1,  3,  5,  6,  8, 10,  7,  9, 11])
    >>> a.ravel(order='K')
    array([ 0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11])

    """
    if isinstance(a, np.matrix):
        return asarray(a).ravel(order=order)
    else:
        return asanyarray(a).ravel(order=order)


def ravel(a: ArrayLike, order: str = "C", *, out_sharding=None) -> Array:
  """Flatten array into a 1-dimensional shape.

  JAX implementation of :func:`numpy.ravel`, implemented in terms of
  :func:`jax.lax.reshape`.

  ``ravel(arr, order=order)`` is equivalent to ``reshape(arr, -1, order=order)``.

  Args:
    a: array to be flattened.
    order: ``'F'`` or ``'C'``, specifies whether the reshape should apply column-major
      (fortran-style, ``"F"``) or row-major (C-style, ``"C"``) order; default is ``"C"``.
      JAX does not support `order="A"` or `order="K"`.

  Returns:
    flattened copy of input array.

  Notes:
    Unlike :func:`numpy.ravel`, :func:`jax.numpy.ravel` will return a copy rather
    than a view of the input array. However, under JIT, the compiler will optimize-away
    such copies when possible, so this doesn't have performance impacts in practice.

  See Also:
    - :meth:`jax.Array.ravel`: equivalent functionality via an array method.
    - :func:`jax.numpy.reshape`: general array reshape.

  Examples:
    >>> x = jnp.array([[1, 2, 3],
    ...                [4, 5, 6]])

    By default, ravel in C-style, row-major order

    >>> jnp.ravel(x)
    Array([1, 2, 3, 4, 5, 6], dtype=int32)

    Optionally ravel in Fortran-style, column-major:

    >>> jnp.ravel(x, order='F')
    Array([1, 4, 2, 5, 3, 6], dtype=int32)

    For convenience, the same functionality is available via the :meth:`jax.Array.ravel`
    method:

    >>> x.ravel()
    Array([1, 2, 3, 4, 5, 6], dtype=int32)
  """
  a = util.ensure_arraylike("ravel", a)
  if order == "K":
    raise NotImplementedError("Ravel not implemented for order='K'.")
  return reshape(a, (np.size(a),), order, out_sharding=out_sharding)

