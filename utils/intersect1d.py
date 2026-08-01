
def intersect1d(ar1, ar2, assume_unique=False, return_indices=False):
    """
    Find the intersection of two arrays.

    Return the sorted, unique values that are in both of the input arrays.

    Parameters
    ----------
    ar1, ar2 : array_like
        Input arrays. Will be flattened if not already 1D.
    assume_unique : bool
        If True, the input arrays are both assumed to be unique, which
        can speed up the calculation.  If True but ``ar1`` or ``ar2`` are not
        unique, incorrect results and out-of-bounds indices could result.
        Default is False.
    return_indices : bool
        If True, the indices which correspond to the intersection of the two
        arrays are returned. The first instance of a value is used if there are
        multiple. Default is False.

    Returns
    -------
    intersect1d : ndarray
        Sorted 1D array of common and unique elements.
    comm1 : ndarray
        The indices of the first occurrences of the common values in `ar1`.
        Only provided if `return_indices` is True.
    comm2 : ndarray
        The indices of the first occurrences of the common values in `ar2`.
        Only provided if `return_indices` is True.

    Examples
    --------
    >>> import numpy as np
    >>> np.intersect1d([1, 3, 4, 3], [3, 1, 2, 1])
    array([1, 3])

    To intersect more than two arrays, use functools.reduce:

    >>> from functools import reduce
    >>> reduce(np.intersect1d, ([1, 3, 4, 3], [3, 1, 2, 1], [6, 3, 4, 2]))
    array([3])

    To return the indices of the values common to the input arrays
    along with the intersected values:

    >>> x = np.array([1, 1, 2, 3, 4])
    >>> y = np.array([2, 1, 4, 6])
    >>> xy, x_ind, y_ind = np.intersect1d(x, y, return_indices=True)
    >>> x_ind, y_ind
    (array([0, 2, 4]), array([1, 0, 2]))
    >>> xy, x[x_ind], y[y_ind]
    (array([1, 2, 4]), array([1, 2, 4]), array([1, 2, 4]))

    """
    ar1 = np.asanyarray(ar1)
    ar2 = np.asanyarray(ar2)

    if not assume_unique:
        if return_indices:
            ar1, ind1 = unique(ar1, return_index=True)
            ar2, ind2 = unique(ar2, return_index=True)
        else:
            ar1 = unique(ar1)
            ar2 = unique(ar2)
    else:
        ar1 = ar1.ravel()
        ar2 = ar2.ravel()

    aux = np.concatenate((ar1, ar2))
    if return_indices:
        aux_sort_indices = np.argsort(aux, kind='mergesort')
        aux = aux[aux_sort_indices]
    else:
        aux.sort()

    mask = aux[1:] == aux[:-1]
    int1d = aux[:-1][mask]

    if return_indices:
        ar1_indices = aux_sort_indices[:-1][mask]
        ar2_indices = aux_sort_indices[1:][mask] - ar1.size
        if not assume_unique:
            ar1_indices = ind1[ar1_indices]
            ar2_indices = ind2[ar2_indices]

        return int1d, ar1_indices, ar2_indices
    else:
        return int1d


def intersect1d(ar1, ar2, assume_unique=False):
    """
    Returns the unique elements common to both arrays.

    Masked values are considered equal one to the other.
    The output is always a masked array.

    See `numpy.intersect1d` for more details.

    See Also
    --------
    numpy.intersect1d : Equivalent function for ndarrays.

    Examples
    --------
    >>> import numpy as np
    >>> x = np.ma.array([1, 3, 3, 3], mask=[0, 0, 0, 1])
    >>> y = np.ma.array([3, 1, 1, 1], mask=[0, 0, 0, 1])
    >>> np.ma.intersect1d(x, y)
    masked_array(data=[1, 3, --],
                 mask=[False, False,  True],
           fill_value=999999)

    """
    if assume_unique:
        aux = ma.concatenate((ar1, ar2))
    else:
        # Might be faster than unique( intersect1d( ar1, ar2 ) )?
        aux = ma.concatenate((unique(ar1), unique(ar2)))
    aux.sort()
    return aux[:-1][aux[1:] == aux[:-1]]


def intersect1d(ar1: ArrayLike, ar2: ArrayLike, assume_unique: bool = False,
                return_indices: bool = False, *, size: int | None = None,
                fill_value: ArrayLike | None = None) -> Array | tuple[Array, Array, Array]:
  """Compute the set intersection of two 1D arrays.

  JAX implementation of :func:`numpy.intersect1d`.

  Because the size of the output of ``intersect1d`` is data-dependent, the function
  is not typically compatible with :func:`~jax.jit` and other JAX transformations.
  The JAX version adds the optional ``size`` argument which must be specified
  statically for ``jnp.intersect1d`` to be used in such contexts.

  Args:
    ar1: first array of values to intersect.
    ar2: second array of values to intersect.
    assume_unique: if True, assume the input arrays contain unique values. This allows
      a more efficient implementation, but if ``assume_unique`` is True and the input
      arrays contain duplicates, the behavior is undefined. default: False.
    return_indices: If True, return arrays of indices specifying where the intersected
      values first appear in the input arrays.
    size: if specified, return only the first ``size`` sorted elements. If there are fewer
      elements than ``size`` indicates, the return value will be padded with ``fill_value``,
      and returned indices will be padded with an out-of-bound index.
    fill_value: when ``size`` is specified and there are fewer than the indicated number of
      elements, fill the remaining entries ``fill_value``. Defaults to the smallest value
      in the intersection.

  Returns:
    An array ``intersection``, or if ``return_indices=True``, a tuple of arrays
    ``(intersection, ar1_indices, ar2_indices)``. Returned values are

    - ``intersection``:
      A 1D array containing each value that appears in both ``ar1`` and ``ar2``.
    - ``ar1_indices``:
      *(returned if return_indices=True)* an array of shape ``intersection.shape`` containing
      the indices in flattened ``ar1`` of values in ``intersection``. For 1D inputs,
      ``intersection`` is equivalent to ``ar1[ar1_indices]``.
    - ``ar2_indices``:
      *(returned if return_indices=True)* an array of shape ``intersection.shape`` containing
      the indices in flattened ``ar2`` of values in ``intersection``. For 1D inputs,
      ``intersection`` is equivalent to ``ar2[ar2_indices]``.

  See also:
    - :func:`jax.numpy.union1d`: the set union of two 1D arrays.
    - :func:`jax.numpy.setxor1d`: the set XOR of two 1D arrays.
    - :func:`jax.numpy.setdiff1d`: the set difference of two 1D arrays.

  Examples:
    >>> ar1 = jnp.array([1, 2, 3, 4])
    >>> ar2 = jnp.array([3, 4, 5, 6])
    >>> jnp.intersect1d(ar1, ar2)
    Array([3, 4], dtype=int32)

    Computing intersection with indices:

    >>> intersection, ar1_indices, ar2_indices = jnp.intersect1d(ar1, ar2, return_indices=True)
    >>> intersection
    Array([3, 4], dtype=int32)

    ``ar1_indices`` gives the indices of the intersected values within ``ar1``:

     >>> ar1_indices
     Array([2, 3], dtype=int32)
     >>> jnp.all(intersection == ar1[ar1_indices])
     Array(True, dtype=bool)

    ``ar2_indices`` gives the indices of the intersected values within ``ar2``:

     >>> ar2_indices
     Array([0, 1], dtype=int32)
     >>> jnp.all(intersection == ar2[ar2_indices])
     Array(True, dtype=bool)
  """
  ar1, ar2 = ensure_arraylike("intersect1d", ar1, ar2)
  arr1, arr2 = promote_dtypes(ar1, ar2)
  del ar1, ar2
  arr1 = ravel(arr1)
  arr2 = ravel(arr2)

  if size is not None:
    return _intersect1d_size(arr1, arr2, return_indices=return_indices,
                             size=size, fill_value=fill_value, assume_unique=assume_unique)

  ind1 = ind2 = arange(0)
  if not assume_unique:
    if return_indices:
      arr1, ind1 = unique(arr1, return_index=True)
      arr2, ind2 = unique(arr2, return_index=True)
    else:
      arr1 = unique(arr1)
      arr2 = unique(arr2)

  aux, mask, aux_sort_indices = _intersect1d_sorted_mask(arr1, arr2, return_indices)

  int1d = aux[:-1][mask]

  if return_indices:
    assert aux_sort_indices is not None
    arr1_indices = aux_sort_indices[:-1][mask]
    arr2_indices = aux_sort_indices[1:][mask] - np.size(arr1)
    if not assume_unique:
      arr1_indices = ind1[arr1_indices]
      arr2_indices = ind2[arr2_indices]
    return int1d, arr1_indices, arr2_indices
  else:
    return int1d

