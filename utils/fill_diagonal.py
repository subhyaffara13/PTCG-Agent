
def fill_diagonal(a: ArrayLike, val: ArrayLike, wrap=False):
    if a.ndim < 2:
        raise ValueError("array must be at least 2-d")
    if val.numel() == 0 and not wrap:
        a.fill_diagonal_(val)
        return a

    if val.ndim == 0:
        val = val.unsqueeze(0)

    # torch.Tensor.fill_diagonal_ only accepts scalars
    # If the size of val is too large, then val is trimmed
    if a.ndim == 2:
        tall = a.shape[0] > a.shape[1]
        # wrap does nothing for wide matrices...
        if not wrap or not tall:
            # Never wraps
            diag = a.diagonal()
            diag.copy_(val[: diag.numel()])
        else:
            # wraps and tall... leaving one empty line between diagonals?!
            max_, min_ = a.shape
            idx = torch.arange(max_ - max_ // (min_ + 1))
            mod = idx % min_
            div = idx // min_
            a[(div * (min_ + 1) + mod, mod)] = val[: idx.numel()]
    else:
        idx = diag_indices_from(a)
        # a.shape = (n, n, ..., n)
        a[idx] = val[: a.shape[0]]

    return a


def fill_diagonal(a, val, wrap=False):
    """Fill the main diagonal of the given array of any dimensionality.

    For an array `a` with ``a.ndim >= 2``, the diagonal is the list of
    values ``a[i, ..., i]`` with indices ``i`` all identical.  This function
    modifies the input array in-place without returning a value.

    Parameters
    ----------
    a : array, at least 2-D.
      Array whose diagonal is to be filled in-place.
    val : scalar or array_like
      Value(s) to write on the diagonal. If `val` is scalar, the value is
      written along the diagonal. If array-like, the flattened `val` is
      written along the diagonal, repeating if necessary to fill all
      diagonal entries.

    wrap : bool
      For tall matrices in NumPy version up to 1.6.2, the
      diagonal "wrapped" after N columns. You can have this behavior
      with this option. This affects only tall matrices.

    See also
    --------
    diag_indices, diag_indices_from

    Notes
    -----
    This functionality can be obtained via `diag_indices`, but internally
    this version uses a much faster implementation that never constructs the
    indices and uses simple slicing.

    Examples
    --------
    >>> import numpy as np
    >>> a = np.zeros((3, 3), int)
    >>> np.fill_diagonal(a, 5)
    >>> a
    array([[5, 0, 0],
           [0, 5, 0],
           [0, 0, 5]])

    The same function can operate on a 4-D array:

    >>> a = np.zeros((3, 3, 3, 3), int)
    >>> np.fill_diagonal(a, 4)

    We only show a few blocks for clarity:

    >>> a[0, 0]
    array([[4, 0, 0],
           [0, 0, 0],
           [0, 0, 0]])
    >>> a[1, 1]
    array([[0, 0, 0],
           [0, 4, 0],
           [0, 0, 0]])
    >>> a[2, 2]
    array([[0, 0, 0],
           [0, 0, 0],
           [0, 0, 4]])

    The wrap option affects only tall matrices:

    >>> # tall matrices no wrap
    >>> a = np.zeros((5, 3), int)
    >>> np.fill_diagonal(a, 4)
    >>> a
    array([[4, 0, 0],
           [0, 4, 0],
           [0, 0, 4],
           [0, 0, 0],
           [0, 0, 0]])

    >>> # tall matrices wrap
    >>> a = np.zeros((5, 3), int)
    >>> np.fill_diagonal(a, 4, wrap=True)
    >>> a
    array([[4, 0, 0],
           [0, 4, 0],
           [0, 0, 4],
           [0, 0, 0],
           [4, 0, 0]])

    >>> # wide matrices
    >>> a = np.zeros((3, 5), int)
    >>> np.fill_diagonal(a, 4, wrap=True)
    >>> a
    array([[4, 0, 0, 0, 0],
           [0, 4, 0, 0, 0],
           [0, 0, 4, 0, 0]])

    The anti-diagonal can be filled by reversing the order of elements
    using either `numpy.flipud` or `numpy.fliplr`.

    >>> a = np.zeros((3, 3), int);
    >>> np.fill_diagonal(np.fliplr(a), [1,2,3])  # Horizontal flip
    >>> a
    array([[0, 0, 1],
           [0, 2, 0],
           [3, 0, 0]])
    >>> np.fill_diagonal(np.flipud(a), [1,2,3])  # Vertical flip
    >>> a
    array([[0, 0, 3],
           [0, 2, 0],
           [1, 0, 0]])

    Note that the order in which the diagonal is filled varies depending
    on the flip function.
    """
    if a.ndim < 2:
        raise ValueError("array must be at least 2-d")
    end = None
    if a.ndim == 2:
        # Explicit, fast formula for the common case.  For 2-d arrays, we
        # accept rectangular ones.
        step = a.shape[1] + 1
        # This is needed to don't have tall matrix have the diagonal wrap.
        if not wrap:
            end = a.shape[1] * a.shape[1]
    else:
        # For more than d=2, the strided formula is only valid for arrays with
        # all dimensions equal, so we check first.
        if not np.all(diff(a.shape) == 0):
            raise ValueError("All dimensions of input must be of equal length")
        step = 1 + (np.cumprod(a.shape[:-1])).sum()

    # Write the value out into the diagonal.
    a.flat[:end:step] = val


def fill_diagonal(a: ArrayLike, val: ArrayLike, wrap: bool = False, *,
                  inplace: bool = True) -> Array:
  """Return a copy of the array with the diagonal overwritten.

  JAX implementation of :func:`numpy.fill_diagonal`.

  The semantics of :func:`numpy.fill_diagonal` are to modify arrays in-place, which
  is not possible for JAX's immutable arrays. The JAX version returns a modified
  copy of the input, and adds the ``inplace`` parameter which must be set to
  `False`` by the user as a reminder of this API difference.

  Args:
    a: input array. Must have ``a.ndim >= 2``. If ``a.ndim >= 3``, then all
      dimensions must be the same size.
    val: scalar or array with which to fill the diagonal. If an array, it will
      be flattened and repeated to fill the diagonal entries.
    wrap: Not implemented by JAX. Only the default value of ``False`` is supported.
    inplace: must be set to False to indicate that the input is not modified
      in-place, but rather a modified copy is returned.

  Returns:
    A copy of ``a`` with the diagonal set to ``val``.

  Examples:
    >>> x = jnp.zeros((3, 3), dtype=int)
    >>> jnp.fill_diagonal(x, jnp.array([1, 2, 3]), inplace=False)
    Array([[1, 0, 0],
           [0, 2, 0],
           [0, 0, 3]], dtype=int32)

    Unlike :func:`numpy.fill_diagonal`, the input ``x`` is not modified.

    If the diagonal value has too many entries, it will be truncated

    >>> jnp.fill_diagonal(x, jnp.arange(100, 200), inplace=False)
    Array([[100,   0,   0],
           [  0, 101,   0],
           [  0,   0, 102]], dtype=int32)

    If the diagonal has too few entries, it will be repeated:

    >>> x = jnp.zeros((4, 4), dtype=int)
    >>> jnp.fill_diagonal(x, jnp.array([3, 4]), inplace=False)
    Array([[3, 0, 0, 0],
           [0, 4, 0, 0],
           [0, 0, 3, 0],
           [0, 0, 0, 4]], dtype=int32)

    For non-square arrays, the diagonal of the leading square slice is filled:

    >>> x = jnp.zeros((3, 5), dtype=int)
    >>> jnp.fill_diagonal(x, 1, inplace=False)
    Array([[1, 0, 0, 0, 0],
           [0, 1, 0, 0, 0],
           [0, 0, 1, 0, 0]], dtype=int32)

    And for square N-dimensional arrays, the N-dimensional diagonal is filled:

    >>> y = jnp.zeros((2, 2, 2))
    >>> jnp.fill_diagonal(y, 1, inplace=False)
    Array([[[1., 0.],
            [0., 0.]],
    <BLANKLINE>
           [[0., 0.],
            [0., 1.]]], dtype=float32)
  """
  if inplace:
    raise NotImplementedError("JAX arrays are immutable, must use inplace=False")
  if wrap:
    raise NotImplementedError("wrap=True is not implemented, must use wrap=False")
  a, val = util.ensure_arraylike("fill_diagonal", a, val)
  if a.ndim < 2:
    raise ValueError("array must be at least 2-d")
  if a.ndim > 2 and not all(n == a.shape[0] for n in a.shape[1:]):
    raise ValueError("All dimensions of input must be of equal length")
  n = min(a.shape)
  idx = diag_indices(n, a.ndim)
  return a.at[idx].set(val if val.ndim == 0 else _tile_to_size(val.ravel(), n))

