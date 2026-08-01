
def setxor1d(ar1, ar2, assume_unique=False):
    """
    Find the set exclusive-or of two arrays.

    Return the sorted, unique values that are in only one (not both) of the
    input arrays.

    Parameters
    ----------
    ar1, ar2 : array_like
        Input arrays.
    assume_unique : bool
        If True, the input arrays are both assumed to be unique, which
        can speed up the calculation. Default is False.

    Returns
    -------
    setxor1d : ndarray
        Sorted 1D array of unique values that are in only one of the input
        arrays.

    Examples
    --------
    >>> import numpy as np
    >>> a = np.array([1, 2, 3, 2, 4])
    >>> b = np.array([2, 3, 5, 7, 5])
    >>> np.setxor1d(a,b)
    array([1, 4, 5, 7])

    """
    if not assume_unique:
        ar1 = unique(ar1)
        ar2 = unique(ar2)

    aux = np.concatenate((ar1, ar2), axis=None)
    if aux.size == 0:
        return aux

    aux.sort()
    flag = np.concatenate(([True], aux[1:] != aux[:-1], [True]))
    return aux[flag[1:] & flag[:-1]]


def setxor1d(ar1, ar2, assume_unique=False):
    """
    Set exclusive-or of 1-D arrays with unique elements.

    The output is always a masked array. See `numpy.setxor1d` for more details.

    See Also
    --------
    numpy.setxor1d : Equivalent function for ndarrays.

    Examples
    --------
    >>> import numpy as np
    >>> ar1 = np.ma.array([1, 2, 3, 2, 4])
    >>> ar2 = np.ma.array([2, 3, 5, 7, 5])
    >>> np.ma.setxor1d(ar1, ar2)
    masked_array(data=[1, 4, 5, 7],
                 mask=False,
           fill_value=999999)

    """
    if not assume_unique:
        ar1 = unique(ar1)
        ar2 = unique(ar2)

    aux = ma.concatenate((ar1, ar2), axis=None)
    if aux.size == 0:
        return aux
    aux.sort()
    auxf = aux.filled()
#    flag = ediff1d( aux, to_end = 1, to_begin = 1 ) == 0
    flag = ma.concatenate(([True], (auxf[1:] != auxf[:-1]), [True]))
#    flag2 = ediff1d( flag ) == 0
    flag2 = (flag[1:] == flag[:-1])
    return aux[flag2]


def setxor1d(ar1: ArrayLike, ar2: ArrayLike, assume_unique: bool = False, *,
             size: int | None = None, fill_value: ArrayLike | None = None) -> Array:
  """Compute the set-wise xor of elements in two arrays.

  JAX implementation of :func:`numpy.setxor1d`.

  Because the size of the output of ``setxor1d`` is data-dependent, the function is not
  compatible with JIT or other JAX transformations.

  Args:
    ar1: first array of values to intersect.
    ar2: second array of values to intersect.
    assume_unique: if True, assume the input arrays contain unique values. This allows
      a more efficient implementation, but if ``assume_unique`` is True and the input
      arrays contain duplicates, the behavior is undefined. default: False.
    size: if specified, return only the first ``size`` sorted elements. If there are fewer
      elements than ``size`` indicates, the return value will be padded with ``fill_value``,
      and returned indices will be padded with an out-of-bound index.
    fill_value: when ``size`` is specified and there are fewer than the indicated number of
      elements, fill the remaining entries ``fill_value``. Defaults to the smallest value
      in the xor result.

  Returns:
    An array of values that are found in exactly one of the input arrays.

  See also:
    - :func:`jax.numpy.intersect1d`: the set intersection of two 1D arrays.
    - :func:`jax.numpy.union1d`: the set union of two 1D arrays.
    - :func:`jax.numpy.setdiff1d`: the set difference of two 1D arrays.

  Examples:
    >>> ar1 = jnp.array([1, 2, 3, 4])
    >>> ar2 = jnp.array([3, 4, 5, 6])
    >>> jnp.setxor1d(ar1, ar2)
    Array([1, 2, 5, 6], dtype=int32)
  """
  ar1, ar2 = ensure_arraylike("setxor1d", ar1, ar2)
  arr1, arr2 = promote_dtypes(ravel(ar1), ravel(ar2))
  del ar1, ar2

  if size is not None:
    return _setxor1d_size(arr1, arr2, fill_value=fill_value,
                          assume_unique=assume_unique, size=size)

  if not assume_unique:
    arr1 = unique(arr1)
    arr2 = unique(arr2)
  aux = concatenate((arr1, arr2))
  if aux.size == 0:
    return aux
  aux = sort(aux)
  flag = concatenate((True, aux[1:] != aux[:-1], True), axis=None)
  return aux[flag[1:] & flag[:-1]]

