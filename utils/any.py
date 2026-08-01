
def any(
    a: ArrayLike,
    axis: AxisLike = None,
    out: OutArray | None = None,
    keepdims: KeepDims = False,
    *,
    where: NotImplementedType = None,
):
    axis = _util.allow_only_single_axis(axis)
    axis_kw = {} if axis is None else {"dim": axis}
    return torch.any(a, **axis_kw)


def any(
    a: TensorLikeType,
    dim: DimsType | None = None,
    keepdim: bool = False,
) -> TensorLikeType:
    a_ = _maybe_convert_to_dtype(a, torch.bool)
    if isinstance(dim, (list, tuple)) and len(dim) == 0:
        result = a_.clone()
    else:
        result = a_.sum(dim=dim, keepdim=keepdim).ne(False)

    # Preserves uint8 -- probably a legacy mask thing
    if a.dtype is torch.uint8:
        return prims.convert_element_type(result, torch.uint8)

    return result


def any(a, dim):
    return tl.reduce(a, dim, _any_combine)


def any(iterable: Iterable[object], /) -> bool:
    for elem in iterable:
        if elem:
            return True
    return False


def any(x: Array,
        /,
        *,
        axis: int | tuple[int, ...] | None = None,
        keepdims: bool = False,
        **kwargs: object) -> Array:

    if axis == ():
        return x.to(torch.bool)
    # torch.any doesn't support multiple axes
    # (https://github.com/pytorch/pytorch/issues/56586).
    if isinstance(axis, tuple):
        res = _reduce_multiple_axes(torch.any, x, axis, keepdims=keepdims, **kwargs)
        return res.to(torch.bool)
    if axis is None:
        # torch doesn't support keepdims with axis=None
        # (https://github.com/pytorch/pytorch/issues/71209)
        res = torch.any(x, **kwargs)
        res = _axis_none_keepdims(res, x.ndim, keepdims)
        return res.to(torch.bool)

    # torch.any doesn't return bool for uint8
    return torch.any(x, axis, keepdims=keepdims).to(torch.bool)


def any(a, axis=None, out=None, keepdims=np._NoValue, *, where=np._NoValue):
    """
    Test whether any array element along a given axis evaluates to True.

    Returns single boolean if `axis` is ``None``

    Parameters
    ----------
    a : array_like
        Input array or object that can be converted to an array.
    axis : None or int or tuple of ints, optional
        Axis or axes along which a logical OR reduction is performed.
        The default (``axis=None``) is to perform a logical OR over all
        the dimensions of the input array. `axis` may be negative, in
        which case it counts from the last to the first axis. If this
        is a tuple of ints, a reduction is performed on multiple
        axes, instead of a single axis or all the axes as before.
    out : ndarray, optional
        Alternate output array in which to place the result.  It must have
        the same shape as the expected output and its type is preserved
        (e.g., if it is of type float, then it will remain so, returning
        1.0 for True and 0.0 for False, regardless of the type of `a`).
        See :ref:`ufuncs-output-type` for more details.

    keepdims : bool, optional
        If this is set to True, the axes which are reduced are left
        in the result as dimensions with size one. With this option,
        the result will broadcast correctly against the input array.

        If the default value is passed, then `keepdims` will not be
        passed through to the `any` method of sub-classes of
        `ndarray`, however any non-default value will be.  If the
        sub-class' method does not implement `keepdims` any
        exceptions will be raised.

    where : array_like of bool, optional
        Elements to include in checking for any `True` values.
        See `~numpy.ufunc.reduce` for details.

        .. versionadded:: 1.20.0

    Returns
    -------
    any : bool or ndarray
        A new boolean or `ndarray` is returned unless `out` is specified,
        in which case a reference to `out` is returned.

    See Also
    --------
    ndarray.any : equivalent method

    all : Test whether all elements along a given axis evaluate to True.

    Notes
    -----
    Not a Number (NaN), positive infinity and negative infinity evaluate
    to `True` because these are not equal to zero.

    .. versionchanged:: 2.0
       Before NumPy 2.0, ``any`` did not return booleans for object dtype
       input arrays.
       This behavior is still available via ``np.logical_or.reduce``.

    Examples
    --------
    >>> import numpy as np
    >>> np.any([[True, False], [True, True]])
    True

    >>> np.any([[True,  False, True ],
    ...         [False, False, False]], axis=0)
    array([ True, False, True])

    >>> np.any([-1, 0, 5])
    True

    >>> np.any([[np.nan], [np.inf]], axis=1, keepdims=True)
    array([[ True],
           [ True]])

    >>> np.any([[True, False], [False, False]], where=[[False], [True]])
    False

    >>> a = np.array([[1, 0, 0],
    ...               [0, 0, 1],
    ...               [0, 0, 0]])
    >>> np.any(a, axis=0)
    array([ True, False,  True])
    >>> np.any(a, axis=1)
    array([ True,  True, False])

    >>> o=np.array(False)
    >>> z=np.any([-1, 4, 5], out=o)
    >>> z, o
    (array(True), array(True))
    >>> # Check now that z is a reference to o
    >>> z is o
    True
    >>> id(z), id(o) # identity of z and o              # doctest: +SKIP
    (191614240, 191614240)

    """
    return _wrapreduction_any_all(a, np.logical_or, 'any', axis, out,
                                  keepdims=keepdims, where=where)


def any(a: ArrayLike, axis: Axis = None, out: None = None,
        keepdims: bool = False, *, where: ArrayLike | None = None) -> Array:
  r"""Test whether any of the array elements along a given axis evaluate to True.

  JAX implementation of :func:`numpy.any`.

  Args:
    a: Input array.
    axis: int or array, default=None. Axis along which to be tested. If None,
      tests along all the axes.
    keepdims: bool, default=False. If true, reduced axes are left in the result
      with size 1.
    where: int or array of boolean dtype, default=None. The elements to be used
      in the test. Array should be broadcast compatible to the input.
    out: Unused by JAX.

  Returns:
    An array of boolean values.

  Examples:
    By default, ``jnp.any`` tests along all the axes.

    >>> x = jnp.array([[True, True, True, False],
    ...                [True, False, True, False],
    ...                [True, True, False, False]])
    >>> jnp.any(x)
    Array(True, dtype=bool)

    If ``axis=0``, tests along axis 0.

    >>> jnp.any(x, axis=0)
    Array([ True,  True,  True, False], dtype=bool)

    If ``keepdims=True``, ``ndim`` of the output will be same of that of the input.

    >>> jnp.any(x, axis=0, keepdims=True)
    Array([[ True,  True,  True, False]], dtype=bool)

    To include specific elements in testing for True values, you can use a``where``.

    >>> where=jnp.array([[1, 0, 1, 0],
    ...                  [0, 1, 0, 1],
    ...                  [1, 0, 1, 0]], dtype=bool)
    >>> jnp.any(x, axis=0, keepdims=True, where=where)
    Array([[ True, False,  True, False]], dtype=bool)
  """
  return _reduce_any(a, axis=_ensure_optional_axes(axis), out=out,
                     keepdims=keepdims, where=where)

