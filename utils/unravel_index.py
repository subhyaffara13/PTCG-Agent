
def unravel_index(
    indices: Tensor,
    shape: int | Sequence[int] | torch.Size,
) -> tuple[Tensor, ...]:
    r"""Converts a tensor of flat indices into a tuple of coordinate tensors that
    index into an arbitrary tensor of the specified shape.

    Args:
        indices (Tensor): An integer tensor containing indices into the
            flattened version of an arbitrary tensor of shape :attr:`shape`.
            All elements must be in the range ``[0, prod(shape) - 1]``.

        shape (int, sequence of ints, or torch.Size): The shape of the arbitrary
            tensor. All elements must be non-negative.

    Returns:
        tuple of Tensors: Each ``i``-th tensor in the output corresponds with
        dimension ``i`` of :attr:`shape`. Each tensor has the same shape as
        ``indices`` and contains one index into dimension ``i`` for each of the
        flat indices given by ``indices``.

    Example::

        >>> import torch
        >>> torch.unravel_index(torch.tensor(4), (3, 2))
        (tensor(2),
         tensor(0))

        >>> torch.unravel_index(torch.tensor([4, 1]), (3, 2))
        (tensor([2, 0]),
         tensor([0, 1]))

        >>> torch.unravel_index(torch.tensor([0, 1, 2, 3, 4, 5]), (3, 2))
        (tensor([0, 0, 1, 1, 2, 2]),
         tensor([0, 1, 0, 1, 0, 1]))

        >>> torch.unravel_index(torch.tensor([1234, 5678]), (10, 10, 10, 10))
        (tensor([1, 5]),
         tensor([2, 6]),
         tensor([3, 7]),
         tensor([4, 8]))

        >>> torch.unravel_index(torch.tensor([[1234], [5678]]), (10, 10, 10, 10))
        (tensor([[1], [5]]),
         tensor([[2], [6]]),
         tensor([[3], [7]]),
         tensor([[4], [8]]))

        >>> torch.unravel_index(torch.tensor([[1234], [5678]]), (100, 100))
        (tensor([[12], [56]]),
         tensor([[34], [78]]))
    """
    if has_torch_function_unary(indices):
        return handle_torch_function(unravel_index, (indices,), indices, shape=shape)
    res_tensor = _unravel_index(indices, shape)
    return res_tensor.unbind(-1)


def unravel_index(indices, shape, order="C"):
    """
    unravel_index(indices, shape, order='C')

    Converts a flat index or array of flat indices into a tuple
    of coordinate arrays.

    Parameters
    ----------
    indices : array_like
        An integer array whose elements are indices into the flattened
        version of an array of dimensions ``shape``. Before version 1.6.0,
        this function accepted just one index value.
    shape : tuple of ints
        The shape of the array to use for unraveling ``indices``.
    order : {'C', 'F'}, optional
        Determines whether the indices should be viewed as indexing in
        row-major (C-style) or column-major (Fortran-style) order.

    Returns
    -------
    unraveled_coords : tuple of ndarray
        Each array in the tuple has the same shape as the ``indices``
        array.

    See Also
    --------
    ravel_multi_index

    Examples
    --------
    >>> import numpy as np
    >>> np.unravel_index([22, 41, 37], (7,6))
    (array([3, 6, 6]), array([4, 5, 1]))
    >>> np.unravel_index([31, 41, 13], (7,6), order='F')
    (array([3, 6, 6]), array([4, 5, 1]))

    >>> np.unravel_index(1621, (6,7,8,9))
    (3, 1, 4, 1)

    """
    return (indices,)


def unravel_index(indices: ArrayLike, shape: Shape) -> tuple[Array, ...]:
  """Convert flat indices into multi-dimensional indices.

  JAX implementation of :func:`numpy.unravel_index`. The JAX version differs in
  its treatment of out-of-bound indices: unlike NumPy, negative indices are
  supported, and out-of-bound indices are clipped to the nearest valid value.

  Args:
    indices: integer array of flat indices
    shape: shape of multidimensional array to index into

  Returns:
    Tuple of unraveled indices

  See also:
    :func:`jax.numpy.ravel_multi_index`: Inverse of this function.

  Examples:
    Start with a 1D array values and indices:

    >>> x = jnp.array([2., 3., 4., 5., 6., 7.])
    >>> indices = jnp.array([1, 3, 5])
    >>> print(x[indices])
    [3. 5. 7.]

    Now if ``x`` is reshaped, ``unravel_indices`` can be used to convert
    the flat indices into a tuple of indices that access the same entries:

    >>> shape = (2, 3)
    >>> x_2D = x.reshape(shape)
    >>> indices_2D = jnp.unravel_index(indices, shape)
    >>> indices_2D
    (Array([0, 1, 1], dtype=int32), Array([1, 0, 2], dtype=int32))
    >>> print(x_2D[indices_2D])
    [3. 5. 7.]

    The inverse function, ``ravel_multi_index``, can be used to obtain the
    original indices:

    >>> jnp.ravel_multi_index(indices_2D, shape)
    Array([1, 3, 5], dtype=int32)
  """
  indices_arr = util.ensure_arraylike("unravel_index", indices)
  # Note: we do not convert shape to an array, because it may be passed as a
  # tuple of weakly-typed values, and asarray() would strip these weak types.
  try:
    shape = list(shape)
  except TypeError:
    # TODO: Consider warning here since shape is supposed to be a sequence, so
    # this should not happen.
    shape = [shape]
  if any(np.ndim(s) != 0 for s in shape):
    raise ValueError("unravel_index: shape should be a scalar or 1D sequence.")
  out_indices: list[ArrayLike] = [0] * len(shape)
  for i, s in reversed(list(enumerate(shape))):
    indices_arr, out_indices[i] = ufuncs.divmod(indices_arr, s)
  oob_pos = indices_arr > 0
  if dtypes.issubdtype(indices_arr.dtype, np.unsignedinteger):
    # Unsigned integers can't be out of bounds at the low end.
    oob_neg = asarray(False)
  else:
    oob_neg = indices_arr < -1
  return tuple(where(oob_pos, s - 1, where(oob_neg, 0, i))
               for s, i in safe_zip(shape, out_indices))

