
def setdiff1d(
    x1: Array | complex,
    x2: Array | complex,
    /,
    *,
    assume_unique: bool = False,
    xp: ModuleType | None = None,
) -> Array:
    """
    Find the set difference of two arrays.

    Return the unique values in `x1` that are not in `x2`.

    Parameters
    ----------
    x1 : array | int | float | complex | bool
        Input array.
    x2 : array
        Input comparison array.
    assume_unique : bool
        If ``True``, the input arrays are both assumed to be unique, which
        can speed up the calculation. Default is ``False``.
    xp : array_namespace, optional
        The standard-compatible namespace for `x1` and `x2`. Default: infer.

    Returns
    -------
    array
        1D array of values in `x1` that are not in `x2`. The result
        is sorted when `assume_unique` is ``False``, but otherwise only sorted
        if the input is sorted.

    Examples
    --------
    >>> import array_api_strict as xp
    >>> import array_api_extra as xpx

    >>> x1 = xp.asarray([1, 2, 3, 2, 4, 1])
    >>> x2 = xp.asarray([3, 4, 5, 6])
    >>> xpx.setdiff1d(x1, x2, xp=xp)
    Array([1, 2], dtype=array_api_strict.int64)
    """

    if xp is None:
        xp = array_namespace(x1, x2)

    if is_numpy_namespace(xp) or is_cupy_namespace(xp) or is_jax_namespace(xp):
        x1, x2 = asarrays(x1, x2, xp=xp)
        return xp.setdiff1d(x1, x2, assume_unique=assume_unique)

    return _funcs.setdiff1d(x1, x2, assume_unique=assume_unique, xp=xp)


def setdiff1d(
    x1: Array | complex,
    x2: Array | complex,
    /,
    *,
    assume_unique: bool = False,
    xp: ModuleType,
) -> Array:  # numpydoc ignore=PR01,RT01
    """See docstring in `array_api_extra._delegation.py`."""

    # https://github.com/microsoft/pyright/issues/10103
    x1_, x2_ = asarrays(x1, x2, xp=xp)

    if assume_unique:
        x1_ = xp.reshape(x1_, (-1,))
        x2_ = xp.reshape(x2_, (-1,))
    else:
        x1_ = xp.unique_values(x1_)
        x2_ = xp.unique_values(x2_)

    return x1_[_helpers.in1d(x1_, x2_, assume_unique=True, invert=True, xp=xp)]


def setdiff1d(ar1, ar2, assume_unique=False):
    """
    Find the set difference of two arrays.

    Return the unique values in `ar1` that are not in `ar2`.

    Parameters
    ----------
    ar1 : array_like
        Input array.
    ar2 : array_like
        Input comparison array.
    assume_unique : bool
        If True, the input arrays are both assumed to be unique, which
        can speed up the calculation.  Default is False.

    Returns
    -------
    setdiff1d : ndarray
        1D array of values in `ar1` that are not in `ar2`. The result
        is sorted when `assume_unique=False`, but otherwise only sorted
        if the input is sorted.

    Examples
    --------
    >>> import numpy as np
    >>> a = np.array([1, 2, 3, 2, 4, 1])
    >>> b = np.array([3, 4, 5, 6])
    >>> np.setdiff1d(a, b)
    array([1, 2])

    """
    if assume_unique:
        ar1 = np.asarray(ar1).ravel()
    else:
        ar1 = unique(ar1)
        ar2 = unique(ar2)
    return ar1[_isin(ar1, ar2, assume_unique=True, invert=True)]


def setdiff1d(ar1, ar2, assume_unique=False):
    """
    Set difference of 1D arrays with unique elements.

    The output is always a masked array. See `numpy.setdiff1d` for more
    details.

    See Also
    --------
    numpy.setdiff1d : Equivalent function for ndarrays.

    Examples
    --------
    >>> import numpy as np
    >>> x = np.ma.array([1, 2, 3, 4], mask=[0, 1, 0, 1])
    >>> np.ma.setdiff1d(x, [1, 2])
    masked_array(data=[3, --],
                 mask=[False,  True],
           fill_value=999999)

    """
    if assume_unique:
        ar1 = ma.asarray(ar1).ravel()
    else:
        ar1 = unique(ar1)
        ar2 = unique(ar2)
    return ar1[in1d(ar1, ar2, assume_unique=True, invert=True)]


def setdiff1d(ar1: ArrayLike, ar2: ArrayLike, assume_unique: bool = False,
              *, size: int | None = None, fill_value: ArrayLike | None = None) -> Array:
  """Compute the set difference of two 1D arrays.

  JAX implementation of :func:`numpy.setdiff1d`.

  Because the size of the output of ``setdiff1d`` is data-dependent, the function
  is not typically compatible with :func:`~jax.jit` and other JAX transformations.
  The JAX version adds the optional ``size`` argument which must be specified statically
  for ``jnp.setdiff1d`` to be used in such contexts.

  Args:
    ar1: first array of elements to be differenced.
    ar2: second array of elements to be differenced.
    assume_unique: if True, assume the input arrays contain unique values. This allows
      a more efficient implementation, but if ``assume_unique`` is True and the input
      arrays contain duplicates, the behavior is undefined. default: False.
    size: if specified, return only the first ``size`` sorted elements. If there are fewer
      elements than ``size`` indicates, the return value will be padded with ``fill_value``.
    fill_value: when ``size`` is specified and there are fewer than the indicated number of
      elements, fill the remaining entries ``fill_value``. Defaults to the minimum value.

  Returns:
    an array containing the set difference of elements in the input array: i.e. the elements
    in ``ar1`` that are not contained in ``ar2``.

  See also:
    - :func:`jax.numpy.intersect1d`: the set intersection of two 1D arrays.
    - :func:`jax.numpy.setxor1d`: the set XOR of two 1D arrays.
    - :func:`jax.numpy.union1d`: the set union of two 1D arrays.

  Examples:
    Computing the set difference of two arrays:

    >>> ar1 = jnp.array([1, 2, 3, 4])
    >>> ar2 = jnp.array([3, 4, 5, 6])
    >>> jnp.setdiff1d(ar1, ar2)
    Array([1, 2], dtype=int32)

    Because the output shape is dynamic, this will fail under :func:`~jax.jit` and other
    transformations:

    >>> jax.jit(jnp.setdiff1d)(ar1, ar2)  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
       ...
    ConcretizationTypeError: Abstract tracer value encountered where concrete value is expected: traced array with shape int32[4].
    The error occurred while tracing the function setdiff1d at /Users/vanderplas/github/jax-ml/jax/jax/_src/numpy/setops.py:64 for jit. This concrete value was not available in Python because it depends on the value of the argument ar1.

    In order to ensure statically-known output shapes, you can pass a static ``size``
    argument:

    >>> jit_setdiff1d = jax.jit(jnp.setdiff1d, static_argnames=['size'])
    >>> jit_setdiff1d(ar1, ar2, size=2)
    Array([1, 2], dtype=int32)

    If ``size`` is too small, the difference is truncated:

    >>> jit_setdiff1d(ar1, ar2, size=1)
    Array([1], dtype=int32)

    If ``size`` is too large, then the output is padded with ``fill_value``:

    >>> jit_setdiff1d(ar1, ar2, size=4, fill_value=0)
    Array([1, 2, 0, 0], dtype=int32)
  """
  arr1, arr2 = ensure_arraylike("setdiff1d", ar1, ar2)
  arr1 = arr1.ravel()
  arr2 = arr2.ravel()

  if size is None:
    core.concrete_or_error(None, ar1, "The error arose in setdiff1d()")
  else:
    size = core.concrete_or_error(operator.index, size, "The error arose in setdiff1d()")
  fill_value = full_like(arr1, fill_value=(0 if fill_value is None else fill_value),
                         shape=())
  if arr1.size == 0:
    return full_like(arr1, fill_value, shape=size or 0)
  if not assume_unique:
    arr1 = cast(Array, unique(arr1, size=size and arr1.size))
  mask = _in1d(arr1, arr2, invert=True, assume_unique=assume_unique)
  if size is None:
    return arr1[mask]
  else:
    if not (assume_unique or size is None):
      # Set mask to zero at locations corresponding to unique() padding.
      n_unique = arr1.size + 1 - (arr1 == arr1[0]).sum()
      mask = where(arange(arr1.size) < n_unique, mask, False)
    return where(arange(size) < mask.sum(), arr1[where(mask, size=size)], fill_value)

