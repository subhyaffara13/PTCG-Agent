
def unstack(x: Array, /, xp: Namespace, *, axis: int = 0) -> tuple[Array, ...]:
    if x.ndim == 0:
        raise ValueError("Input array must be at least 1-d.")
    return tuple(xp.moveaxis(x, axis, 0))


def unstack(obj: Series, level, fill_value=..., sort: bool = ...) -> DataFrame: ...


def unstack(
    obj: Series | DataFrame, level, fill_value=..., sort: bool = ...
) -> Series | DataFrame: ...


def unstack(
    obj: Series | DataFrame, level, fill_value=None, sort: bool = True
) -> Series | DataFrame:
    if isinstance(level, (tuple, list)):
        if len(level) != 1:
            # _unstack_multiple only handles MultiIndexes,
            # and isn't needed for a single level
            return _unstack_multiple(obj, level, fill_value=fill_value, sort=sort)
        else:
            level = level[0]

    if not is_integer(level) and not level == "__placeholder__":
        # check if level is valid in case of regular index
        obj.index._get_level_number(level)

    if isinstance(obj, DataFrame):
        if isinstance(obj.index, MultiIndex):
            return _unstack_frame(obj, level, fill_value=fill_value, sort=sort)
        else:
            return obj.T.stack()
    elif not isinstance(obj.index, MultiIndex):
        # GH 36113
        # Give nicer error messages when unstack a Series whose
        # Index is not a MultiIndex.
        raise ValueError(
            f"index must be a MultiIndex to unstack, {type(obj.index)} was passed"
        )
    else:
        if is_1d_only_ea_dtype(obj.dtype):
            return _unstack_extension_series(obj, level, fill_value, sort=sort)
        unstacker = _Unstacker(
            obj.index, level=level, constructor=obj._constructor_expanddim, sort=sort
        )
        return unstacker.get_result(obj, value_columns=None, fill_value=fill_value)


def unstack(x, /, *, axis=0):
    """
    Split an array into a sequence of arrays along the given axis.

    The ``axis`` parameter specifies the dimension along which the array will
    be split. For example, if ``axis=0`` (the default) it will be the first
    dimension and if ``axis=-1`` it will be the last dimension.

    The result is a tuple of arrays split along ``axis``.

    .. versionadded:: 2.1.0

    Parameters
    ----------
    x : ndarray
        The array to be unstacked.
    axis : int, optional
        Axis along which the array will be split. Default: ``0``.

    Returns
    -------
    unstacked : tuple of ndarrays
        The unstacked arrays.

    See Also
    --------
    stack : Join a sequence of arrays along a new axis.
    concatenate : Join a sequence of arrays along an existing axis.
    block : Assemble an nd-array from nested lists of blocks.
    split : Split array into a list of multiple sub-arrays of equal size.

    Notes
    -----
    ``unstack`` serves as the reverse operation of :py:func:`stack`, i.e.,
    ``stack(unstack(x, axis=axis), axis=axis) == x``.

    This function is equivalent to ``tuple(np.moveaxis(x, axis, 0))``, since
    iterating on an array iterates along the first axis.

    Examples
    --------
    >>> arr = np.arange(24).reshape((2, 3, 4))
    >>> np.unstack(arr)
    (array([[ 0,  1,  2,  3],
            [ 4,  5,  6,  7],
            [ 8,  9, 10, 11]]),
     array([[12, 13, 14, 15],
            [16, 17, 18, 19],
            [20, 21, 22, 23]]))
    >>> np.unstack(arr, axis=1)
    (array([[ 0,  1,  2,  3],
            [12, 13, 14, 15]]),
     array([[ 4,  5,  6,  7],
            [16, 17, 18, 19]]),
     array([[ 8,  9, 10, 11],
            [20, 21, 22, 23]]))
    >>> arr2 = np.stack(np.unstack(arr, axis=1), axis=1)
    >>> arr2.shape
    (2, 3, 4)
    >>> np.all(arr == arr2)
    np.True_

    """
    if x.ndim == 0:
        raise ValueError("Input array must be at least 1-d.")
    return tuple(_nx.moveaxis(x, axis, 0))


def unstack(x: ArrayLike, axis: int = 0) -> tuple[Array, ...]:
  """Unstacks an array along an axis.

  Args:
    x: the array to unstack.
    axis: the axis along which to unstack the array.

  Returns:
    A tuple of arrays, split along `axis`.

  Examples:
    >>> import jax.numpy as jnp
    >>> from jax import lax
    >>> x = jnp.array([[1, 2], [3, 4]])
    >>> lax.unstack(x, axis=0)
    (Array([1, 2], dtype=int32), Array([3, 4], dtype=int32))
    >>> lax.unstack(x, axis=1)
    (Array([1, 3], dtype=int32), Array([2, 4], dtype=int32))
  """
  arr = asarray(x)
  axis = canonicalize_axis(axis, arr.ndim)
  return tuple(unstack_p.bind(arr, axis=axis))


def unstack(x: ArrayLike, /, *, axis: int = 0) -> tuple[Array, ...]:
  """Unstack an array along an axis.

  JAX implementation of :func:`array_api.unstack`.

  Args:
    x: array to unstack. Must have ``x.ndim >= 1``.
    axis: integer axis along which to unstack. Must satisfy
      ``-x.ndim <= axis < x.ndim``.

  Returns:
    tuple of unstacked arrays.

  See also:
    - :func:`jax.numpy.stack`: inverse of ``unstack``
    - :func:`jax.numpy.split`: split array into batches along an axis.

  Examples:
    >>> arr = jnp.array([[1, 2, 3],
    ...                  [4, 5, 6]])
    >>> arrs = jnp.unstack(arr)
    >>> print(*arrs)
    [1 2 3] [4 5 6]

    :func:`~jax.numpy.stack` provides the inverse of this:

    >>> jnp.stack(arrs)
    Array([[1, 2, 3],
           [4, 5, 6]], dtype=int32)
  """
  x = util.ensure_arraylike("unstack", x)
  return lax.unstack(x, axis=axis)

