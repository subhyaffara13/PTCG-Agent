
def all(
    a: ArrayLike,
    axis: AxisLike = None,
    out: OutArray | None = None,
    keepdims: KeepDims = False,
    *,
    where: NotImplementedType = None,
):
    axis = _util.allow_only_single_axis(axis)
    axis_kw = {} if axis is None else {"dim": axis}
    return torch.all(a, **axis_kw)


def all(
    a: TensorLikeType,
    dim: DimsType | None = None,
    keepdim: bool = False,
) -> TensorLikeType:
    result = torch.logical_not(torch.any(torch.logical_not(a), dim, keepdim=keepdim))

    if a.dtype == torch.uint8:
        result = result.to(dtype=torch.uint8)

    return result


def all(iterable: Iterable[object], /) -> bool:
    for elem in iterable:
        if not elem:
            return False
    return True


def all(x: Array,
        /,
        *,
        axis: int | tuple[int, ...] | None = None,
        keepdims: bool = False,
        **kwargs: object) -> Array:

    if axis == ():
        return x.to(torch.bool)
    # torch.all doesn't support multiple axes
    # (https://github.com/pytorch/pytorch/issues/56586).
    if isinstance(axis, tuple):
        res = _reduce_multiple_axes(torch.all, x, axis, keepdims=keepdims, **kwargs)
        return res.to(torch.bool)
    if axis is None:
        # torch doesn't support keepdims with axis=None
        # (https://github.com/pytorch/pytorch/issues/71209)
        res = torch.all(x, **kwargs)
        res = _axis_none_keepdims(res, x.ndim, keepdims)
        return res.to(torch.bool)

    # torch.all doesn't return bool for uint8
    return torch.all(x, axis, keepdims=keepdims).to(torch.bool)


def all(a, axis=None, out=None, keepdims=np._NoValue, *, where=np._NoValue):
    """
    Test whether all array elements along a given axis evaluate to True.

    Parameters
    ----------
    a : array_like
        Input array or object that can be converted to an array.
    axis : None or int or tuple of ints, optional
        Axis or axes along which a logical AND reduction is performed.
        The default (``axis=None``) is to perform a logical AND over all
        the dimensions of the input array. `axis` may be negative, in
        which case it counts from the last to the first axis. If this
        is a tuple of ints, a reduction is performed on multiple
        axes, instead of a single axis or all the axes as before.
    out : ndarray, optional
        Alternate output array in which to place the result.
        It must have the same shape as the expected output and its
        type is preserved (e.g., if ``dtype(out)`` is float, the result
        will consist of 0.0's and 1.0's). See :ref:`ufuncs-output-type`
        for more details.

    keepdims : bool, optional
        If this is set to True, the axes which are reduced are left
        in the result as dimensions with size one. With this option,
        the result will broadcast correctly against the input array.

        If the default value is passed, then `keepdims` will not be
        passed through to the `all` method of sub-classes of
        `ndarray`, however any non-default value will be.  If the
        sub-class' method does not implement `keepdims` any
        exceptions will be raised.

    where : array_like of bool, optional
        Elements to include in checking for all `True` values.
        See `~numpy.ufunc.reduce` for details.

        .. versionadded:: 1.20.0

    Returns
    -------
    all : ndarray, bool
        A new boolean or array is returned unless `out` is specified,
        in which case a reference to `out` is returned.

    See Also
    --------
    ndarray.all : equivalent method

    any : Test whether any element along a given axis evaluates to True.

    Notes
    -----
    Not a Number (NaN), positive infinity and negative infinity
    evaluate to `True` because these are not equal to zero.

    .. versionchanged:: 2.0
       Before NumPy 2.0, ``all`` did not return booleans for object dtype
       input arrays.
       This behavior is still available via ``np.logical_and.reduce``.

    Examples
    --------
    >>> import numpy as np
    >>> np.all([[True,False],[True,True]])
    False

    >>> np.all([[True,False],[True,True]], axis=0)
    array([ True, False])

    >>> np.all([-1, 4, 5])
    True

    >>> np.all([1.0, np.nan])
    True

    >>> np.all([[True, True], [False, True]], where=[[True], [False]])
    True

    >>> o=np.array(False)
    >>> z=np.all([-1, 4, 5], out=o)
    >>> id(z), id(o), z
    (28293632, 28293632, array(True)) # may vary

    """
    return _wrapreduction_any_all(a, np.logical_and, 'all', axis, out,
                                  keepdims=keepdims, where=where)


def all(tree: Any, *, is_leaf: Callable[[Any], bool] | None = None) -> bool:
  """Call all() over the leaves of a tree.

  Args:
    tree: the pytree to evaluate
    is_leaf : an optionally specified function that will be called at each
      flattening step. It should return a boolean, which indicates whether the
      flattening should traverse the current object, or if it should be stopped
      immediately, with the whole subtree being treated as a leaf.

  Returns:
    result: boolean True or False

  Examples:
    >>> import jax
    >>> jax.tree.all([True, {'a': True, 'b': (True, True)}])
    True
    >>> jax.tree.all([False, (True, False)])
    False

  See Also:
    - :func:`jax.tree.reduce`
    - :func:`jax.tree.leaves`
  """
  return tree_util.tree_all(tree, is_leaf=is_leaf)


def all(a: ArrayLike, axis: Axis = None, out: None = None,
        keepdims: bool = False, *, where: ArrayLike | None = None) -> Array:
  r"""Test whether all array elements along a given axis evaluate to True.

  JAX implementation of :func:`numpy.all`.

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
    By default, ``jnp.all`` tests for True values along all the axes.

    >>> x = jnp.array([[True, True, True, False],
    ...                [True, False, True, False],
    ...                [True, True, False, False]])
    >>> jnp.all(x)
    Array(False, dtype=bool)

    If ``axis=0``, tests for True values along axis 0.

    >>> jnp.all(x, axis=0)
    Array([ True, False, False, False], dtype=bool)

    If ``keepdims=True``, ``ndim`` of the output will be same of that of the input.

    >>> jnp.all(x, axis=0, keepdims=True)
    Array([[ True, False, False, False]], dtype=bool)

    To include specific elements in testing for True values, you can use a``where``.

    >>> where=jnp.array([[1, 0, 1, 0],
    ...                  [0, 0, 1, 1],
    ...                  [1, 1, 1, 0]], dtype=bool)
    >>> jnp.all(x, axis=0, keepdims=True, where=where)
    Array([[ True,  True, False, False]], dtype=bool)
  """
  return _reduce_all(a, axis=_ensure_optional_axes(axis), out=out,
                     keepdims=keepdims, where=where)

