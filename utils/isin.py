
def isin(elements, test_elements, *, assume_unique=False, invert=False):
    # handle when either elements or test_elements are Scalars (they can't both be)
    if not isinstance(elements, torch.Tensor):
        elements = torch.scalar_tensor(elements, device=test_elements.device)
    if not isinstance(test_elements, torch.Tensor):
        if invert:
            return torch.ne(elements, test_elements)
        else:
            return torch.eq(elements, test_elements)

    from torch.fx.experimental.symbolic_shapes import guard_or_false

    if guard_or_false(test_elements.numel() < 10.0 * pow(elements.numel(), 0.145)):
        return isin_default(elements, test_elements, invert=invert)
    else:
        return isin_sorting(
            elements, test_elements, assume_unique=assume_unique, invert=invert
        )


def isin(
    a: Array,
    b: Array,
    /,
    *,
    assume_unique: bool = False,
    invert: bool = False,
    kind: str | None = None,
    xp: ModuleType | None = None,
) -> Array:
    """
    Determine whether each element in `a` is present in `b`.

    Return a boolean array of the same shape as `a` that is True for elements
    that are in `b` and False otherwise.

    Parameters
    ----------
    a : array
        Input elements.
    b : array
        The elements against which to test each element of `a`.
    assume_unique : bool, optional
        If True, the input arrays are both assumed to be unique which can speed
        up the calculation. Default: False.
    invert : bool, optional
        If True, the values in the returned array are inverted. Default: False.
    kind : str | None, optional
        The algorithm or method to use. This will not affect the final result,
        but will affect the speed and memory use.
        For NumPy the options are {None, "sort", "table"}.
        For Jax the mapped parameter is instead `method` and the options are
        {"compare_all", "binary_search", "sort", and "auto" (default)}
        For CuPy, Dask, Torch and the default case this parameter is not present and
        thus ignored. Default: None.
    xp : array_namespace, optional
        The standard-compatible namespace for `a` and `b`. Default: infer.

    Returns
    -------
    array
        An array having the same shape as that of `a` that is True for elements
        that are in `b` and False otherwise.
    """
    if xp is None:
        xp = array_namespace(a, b)

    if is_numpy_namespace(xp):
        return xp.isin(a, b, assume_unique=assume_unique, invert=invert, kind=kind)
    if is_jax_namespace(xp):
        if kind is None:
            kind = "auto"
        return xp.isin(a, b, assume_unique=assume_unique, invert=invert, method=kind)
    if is_cupy_namespace(xp) or is_torch_namespace(xp) or is_dask_namespace(xp):
        return xp.isin(a, b, assume_unique=assume_unique, invert=invert)

    return _funcs.isin(a, b, assume_unique=assume_unique, invert=invert, xp=xp)


def isin(  # numpydoc ignore=PR01,RT01
    a: Array,
    b: Array,
    /,
    *,
    assume_unique: bool = False,
    invert: bool = False,
    xp: ModuleType,
) -> Array:
    """See docstring in `array_api_extra._delegation.py`."""
    original_a_shape = a.shape
    a = xp.reshape(a, (-1,))
    b = xp.reshape(b, (-1,))
    return xp.reshape(
        _helpers.in1d(a, b, assume_unique=assume_unique, invert=invert, xp=xp),
        original_a_shape,
    )


def isin(x1: Array | int, x2: Array | int, /, *, invert: bool = False, **kwds) -> Array:
    if isinstance(x1, int):
        x1 = cp.asarray(x1)
    if isinstance(x2, int):
        x2 = cp.asarray(x2)
    return cp.isin(x1, x2, invert=invert, **kwds)


def isin(comps: ListLike, values: ListLike) -> npt.NDArray[np.bool_]:
    """
    Compute the isin boolean array.

    Parameters
    ----------
    comps : list-like
    values : list-like

    Returns
    -------
    ndarray[bool]
        Same length as `comps`.
    """
    if not is_list_like(comps):
        raise TypeError(
            "only list-like objects are allowed to be passed "
            f"to isin(), you passed a `{type(comps).__name__}`"
        )
    if not is_list_like(values):
        raise TypeError(
            "only list-like objects are allowed to be passed "
            f"to isin(), you passed a `{type(values).__name__}`"
        )

    if not isinstance(values, (ABCIndex, ABCSeries, ABCExtensionArray, np.ndarray)):
        orig_values = list(values)
        values = _ensure_arraylike(orig_values, func_name="isin-targets")

        if (
            len(values) > 0
            and values.dtype.kind in "iufcb"
            and not is_signed_integer_dtype(comps)
            and not is_dtype_equal(values, comps)
        ):
            # GH#46485 Use object to avoid upcast to float64 later
            # TODO: Share with _find_common_type_compat
            values = construct_1d_object_array_from_listlike(orig_values)

    elif isinstance(values, ABCMultiIndex):
        # Avoid raising in extract_array
        values = np.array(values)
    else:
        values = extract_array(values, extract_numpy=True, extract_range=True)

    comps_array = _ensure_arraylike(comps, func_name="isin")
    comps_array = extract_array(comps_array, extract_numpy=True)
    if not isinstance(comps_array, np.ndarray):
        # i.e. Extension Array
        return comps_array.isin(values)

    elif needs_i8_conversion(comps_array.dtype):
        # Dispatch to DatetimeLikeArrayMixin.isin
        return pd_array(comps_array).isin(values)
    elif needs_i8_conversion(values.dtype) and not is_object_dtype(comps_array.dtype):
        # e.g. comps_array are integers and values are datetime64s
        return np.zeros(comps_array.shape, dtype=bool)
        # TODO: not quite right ... Sparse/Categorical
    elif needs_i8_conversion(values.dtype):
        return isin(comps_array, values.astype(object))

    elif isinstance(values.dtype, ExtensionDtype):
        return isin(np.asarray(comps_array), np.asarray(values))

    # GH16012
    # Ensure np.isin doesn't get object types or it *may* throw an exception
    # Albeit hashmap has O(1) look-up (vs. O(logn) in sorted array),
    # isin is faster for small sizes

    # GH60678
    # Ensure values don't contain <NA>, otherwise it throws exception with np.in1d

    if (
        len(comps_array) > _MINIMUM_COMP_ARR_LEN
        and len(values) <= 26
        and comps_array.dtype != object
        and not any(v is NA for v in values)
    ):
        # If the values include nan we need to check for nan explicitly
        # since np.nan it not equal to np.nan
        if isna(values).any():

            def f(c, v):
                return np.logical_or(np.isin(c, v).ravel(), np.isnan(c))

        else:
            f = lambda a, b: np.isin(a, b).ravel()

    else:
        common = np_find_common_type(values.dtype, comps_array.dtype)
        values = values.astype(common, copy=False)
        comps_array = comps_array.astype(common, copy=False)
        f = htable.ismember

    return f(comps_array, values)


def isin(element, test_elements, assume_unique=False, invert=False, *,
         kind=None):
    """
    Calculates ``element in test_elements``, broadcasting over `element` only.
    Returns a boolean array of the same shape as `element` that is True
    where an element of `element` is in `test_elements` and False otherwise.

    Parameters
    ----------
    element : array_like
        Input array.
    test_elements : array_like
        The values against which to test each value of `element`.
        This argument is flattened if it is an array or array_like.
        See notes for behavior with non-array-like parameters.
    assume_unique : bool, optional
        If True, the input arrays are both assumed to be unique, which
        can speed up the calculation.  Default is False.
    invert : bool, optional
        If True, the values in the returned array are inverted, as if
        calculating `element not in test_elements`. Default is False.
        ``np.isin(a, b, invert=True)`` is equivalent to (but faster
        than) ``np.invert(np.isin(a, b))``.
    kind : {None, 'sort', 'table'}, optional
        The algorithm to use. This will not affect the final result,
        but will affect the speed and memory use. The default, None,
        will select automatically based on memory considerations.

        * If 'sort', will use a mergesort-based approach. This will have
          a memory usage of roughly 6 times the sum of the sizes of
          `element` and `test_elements`, not accounting for size of dtypes.
        * If 'table', will use a lookup table approach similar
          to a counting sort. This is only available for boolean and
          integer arrays. This will have a memory usage of the
          size of `element` plus the max-min value of `test_elements`.
          `assume_unique` has no effect when the 'table' option is used.
        * If None, will automatically choose 'table' if
          the required memory allocation is less than or equal to
          6 times the sum of the sizes of `element` and `test_elements`,
          otherwise will use 'sort'. This is done to not use
          a large amount of memory by default, even though
          'table' may be faster in most cases. If 'table' is chosen,
          `assume_unique` will have no effect.


    Returns
    -------
    isin : ndarray, bool
        Has the same shape as `element`. The values `element[isin]`
        are in `test_elements`.

    Notes
    -----
    `isin` is an element-wise function version of the python keyword `in`.
    ``isin(a, b)`` is roughly equivalent to
    ``np.array([item in b for item in a])`` if `a` and `b` are 1-D sequences.

    `element` and `test_elements` are converted to arrays if they are not
    already. If `test_elements` is a set (or other non-sequence collection)
    it will be converted to an object array with one element, rather than an
    array of the values contained in `test_elements`. This is a consequence
    of the `array` constructor's way of handling non-sequence collections.
    Converting the set to a list usually gives the desired behavior.

    Using ``kind='table'`` tends to be faster than `kind='sort'` if the
    following relationship is true:
    ``log10(len(test_elements)) >
    (log10(max(test_elements)-min(test_elements)) - 2.27) / 0.927``,
    but may use greater memory. The default value for `kind` will
    be automatically selected based only on memory usage, so one may
    manually set ``kind='table'`` if memory constraints can be relaxed.

    Examples
    --------
    >>> import numpy as np
    >>> element = 2*np.arange(4).reshape((2, 2))
    >>> element
    array([[0, 2],
           [4, 6]])
    >>> test_elements = [1, 2, 4, 8]
    >>> mask = np.isin(element, test_elements)
    >>> mask
    array([[False,  True],
           [ True, False]])
    >>> element[mask]
    array([2, 4])

    The indices of the matched values can be obtained with `nonzero`:

    >>> np.nonzero(mask)
    (array([0, 1]), array([1, 0]))

    The test can also be inverted:

    >>> mask = np.isin(element, test_elements, invert=True)
    >>> mask
    array([[ True, False],
           [False,  True]])
    >>> element[mask]
    array([0, 6])

    Because of how `array` handles sets, the following does not
    work as expected:

    >>> test_set = {1, 2, 4, 8}
    >>> np.isin(element, test_set)
    array([[False, False],
           [False, False]])

    Casting the set to a list gives the expected result:

    >>> np.isin(element, list(test_set))
    array([[False,  True],
           [ True, False]])
    """
    element = np.asarray(element)
    return _isin(element, test_elements, assume_unique=assume_unique,
                 invert=invert, kind=kind).reshape(element.shape)


def isin(element, test_elements, assume_unique=False, invert=False):
    """
    Calculates `element in test_elements`, broadcasting over
    `element` only.

    The output is always a masked array of the same shape as `element`.
    See `numpy.isin` for more details.

    See Also
    --------
    in1d       : Flattened version of this function.
    numpy.isin : Equivalent function for ndarrays.

    Examples
    --------
    >>> import numpy as np
    >>> element = np.ma.array([1, 2, 3, 4, 5, 6])
    >>> test_elements = [0, 2]
    >>> np.ma.isin(element, test_elements)
    masked_array(data=[False,  True, False, False, False, False],
                 mask=False,
           fill_value=True)

    """
    element = ma.asarray(element)
    return in1d(element, test_elements, assume_unique=assume_unique,
                invert=invert).reshape(element.shape)


def isin(element: ArrayLike, test_elements: ArrayLike,
         assume_unique: bool = False, invert: bool = False, *,
         method='auto') -> Array:
  """Determine whether elements in ``element`` appear in ``test_elements``.

  JAX implementation of :func:`numpy.isin`.

  Args:
    element: input array of elements for which membership will be checked.
    test_elements: N-dimensional array of test values to check for the presence of
      each element.
    invert: If True, return ``~isin(element, test_elements)``. Default is False.
    assume_unique: if true, input arrays are assumed to be unique, which can
      lead to more efficient computation. If the input arrays are not unique
      and assume_unique is set to True, the results are undefined.
    method: string specifying the method used to compute the result. Supported
      options are 'compare_all', 'binary_search', 'sort', and 'auto' (default).

  Returns:
    A boolean array of shape ``element.shape`` that specifies whether each element
    appears in ``test_elements``.

  Examples:
    >>> elements = jnp.array([1, 2, 3, 4])
    >>> test_elements = jnp.array([[1, 5, 6, 3, 7, 1]])
    >>> jnp.isin(elements, test_elements)
    Array([ True, False,  True, False], dtype=bool)
  """
  element, test_elements = ensure_arraylike("isin", element, test_elements)
  result = _in1d(element, test_elements, invert=invert,
                 method=method, assume_unique=assume_unique)
  return result.reshape(np.shape(element))

